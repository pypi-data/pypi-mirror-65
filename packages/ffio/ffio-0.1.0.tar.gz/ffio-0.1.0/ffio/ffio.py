"""
Main module.

This module provides wrappers for reading (ie. **FFReader**) and
writing (ie. **FFWriter**) video files using the common multimedia streamer, ffmpeg.

See Also:
    ffmpeg: https://www.ffmpeg.org/

"""

import numpy as np
import os
import re
import subprocess as sp

FFMPEG_BIN = "ffmpeg" # on Linux and Mac OS

class FFReader(object):
    """The FFReader class provides a wrapper for reading videos with ffmpeg.

    Initialize a reading stream with ffmpeg.

    Start an ffmpeg reader and pipe the raw output directly to a buffer.

    Args:
        path (str): The path to the video file
        custom_size (tuple): height, width tuple of the desired stream size, defaults to the video size
        custom_fps (int): fps to read the stream, defaults to the video fps
        verbose (`bool`, optional): Verbosity flag specifing if debug
            information should be printed.

    Attributes:
        height (int): Height of video in pixels
        width (int): Width of video in pixels
        pipe (sp.Popen): Direct access to the processing stream
        frame_num (int): The index of the last frame to be read

    """

    def __init__(self, path, custom_size=False, custom_fps=False, verbose=False):

        self.path = path
        self.info = self.get_info()
        self.height, self.width = self.get_dims() if not custom_size else custom_size
        self.custom_size = custom_size
        self.fps = self.get_fps()
        self.custom_fps = self.fps if not custom_fps else custom_fps

        self.verbose = verbose
        command = [FFMPEG_BIN]
        command += ['-i', str(path)]
        if custom_fps:
            command += ['-vf', 'fps=fps={}'.format(self.custom_fps)]
        if custom_size:
            command += ['-s', '{}x{}'.format(self.width, self.height)]
        command += ['-f', 'image2pipe']
        command += ['-pix_fmt', 'bgr24']
        command += ['-vcodec', 'rawvideo']
        command += ['-'] #feed input as a stream through python

        if verbose: print("COMMAND: ", command)
        pipe_err = None if verbose else open(os.devnull, 'w')
        self.pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8, stderr=pipe_err)

        self.frame_num = -1

    def read(self):
        """Reads the next image in the buffer

        Returns:
            ret (bool): Successful flag
            image (np.array): Image if successful

        """

        raw_image = self.pipe.stdout.read(self.height*self.width*3)
        self.image =  np.fromstring(raw_image, dtype='uint8')
        if self.image.size == self.width*self.height*3:
            self.image = self.image.reshape((self.height,self.width,3))
            self.pipe.stdout.flush()
            self.frame_num += self.fps/self.custom_fps
            ret = True
        else:
            ret = False
        return (ret, self.image)

    def get_info(self):
        """Reads the info stream from the ffmpeg buffer

        Runs `ffmpeg -i /path/to/video -` under the hood and returns the output

        Returns:
            info (str): Entire information string returned from ffmpeg

        """

        if not hasattr(self, 'info'):
            command = [FFMPEG_BIN,'-i', self.path, '-']
            pipe = sp.Popen(command, stderr=sp.PIPE)
            info = pipe.stderr.read().decode("utf-8")
            pipe.kill()
            return info
        else:
            return self.info

    def get_dims(self):
        """Get the dimensions of the images inside the video

        Obtained by searching through the ffmpeg video info

        Returns:
            dim (tuple): tuple containing:

            - **height** (*int*): height in pixels
            - **width** (*int*): height in pixels

        """

        self.info = self.get_info()
        search = re.search("Stream.*Video.*, (\d+)x(\d+)",self.info)
        width = int(search.group(1))
        height = int(search.group(2))
        return (height,width)

    def get_fps(self):
        """Get the frames per sec of the video

        Obtained by searching through the ffmpeg video info

        Returns:
            fps (int): Frames per second.

        """

        self.info = self.get_info()
        search = re.search(", (\d+(\.(\d+)?)?) fps,",self.info)
        return float(search.group(1))

    def frame_to_secs(self, frame_num):
        """Convert a frame number to seconds into the video

        Args:
            frame_num (int): The number of frames into  (starts at 0).

        Returns:
            secs (float): Seconds into the video.

        """

        fps = self.get_fps()
        return float(frame_num) / fps

    def get_duration(self):
        """Get the duration of the video in seconds

        Returns:
            secs (float): Duration of the video in seconds.

        """

        self.info = self.get_info()
        search = re.search("Duration: (\d+):(\d+):(\d+).(\d+),",self.info)
        hours = int(search.group(1))
        mins = int(search.group(2))
        secs = float(search.group(3)+'.'+search.group(4))

        return secs + 60*(mins + 60*hours)

    def get_total_frames(self):
        """Get the total number of frames in the video

        Returns:
            frames (int): Total number of frames in the video.

        """

        return int(self.get_duration() * self.get_fps()) # FIXME: DOES NOT ACCOUNT FOR CUSTOM_FPS

    def seek(self,sec):
        """Seek to a new part of the video.

        Kills the old ffmpeg pipe and dumps the buffer. Restarts a new pipe
        which starts at the new location, `sec`, and updates `frame_num`
        appropriately.

        Args:
            sec (float): Number of seconds into the video to seek.

        Returns:
            None

        """

        self.release()

        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        time = "%02d:%02d:%05.5f" % (h, m, s)

        command = [ FFMPEG_BIN]
        command += ['-ss', str(time)]
        command += ['-i', str(self.path)]
        if self.custom_fps:
            command += ['-vf', 'fps=fps={}'.format(self.custom_fps)]
        if self.custom_size:
            command += ['-s', '{}x{}'.format(self.width, self.height)]
        command += ['-f', 'image2pipe']
        command += ['-pix_fmt', 'bgr24']
        command += ['-vcodec', 'rawvideo']
        command += ['-']

        if self.verbose: print("COMMAND: ", command)
        pipe_err = None if self.verbose else open(os.devnull, 'w')
        self.pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8, stderr=pipe_err)

        self.frame_num = int(self.get_fps()*sec)-1

    def release(self):
        """Release the FFReader.

        Kills the process and dumps the buffer.

        Returns:
            None

        """

        self.pipe.terminate()
        try:
            self.pipe.stdout.close()
            if self.pipe.stderr:
                self.pipe.stderr.close()
        except IOError:
            pass
        self.pipe.kill()
        self.pipe.wait()

    def close(self):
        """Alias for `release()`.

        Returns:
            None

        """

        self.release()


class FFWriter:
    """The FFWriter class provides a wrapper for writing videos with ffmpeg."""

    def __init__(self, path, height, width,
             codec='libx264', #huffyuv or libx264
             preset='veryslow', #veryslow or veryfast, tradeoff with size
             lossless=False, #use lossless preset
             crf=None, #constant rate factor (0=lossless, 51=worst)
             fps=30,
             verbose=False,
        ):
        """Initialize a writing stream with ffmpeg.

        Start an ffmpeg writer by piping all inputs as raw output directly to
        a buffer.

        Args:
            path (str): The path of the new video file
            height (int): Height of video in pixels
            width (int): Width of video in pixels
            codec (`str`, optional): Codec to write with (default: libx264)
            preset (`str`, optional): ffmpeg preset for writing. Speed
                tradeoff with compression amount (default: veryslow)
            lossless (`bool`, optional): Flag to write lossless video.
                (default: False)
            crf (`int`, optional): ffmpeg constant rate factors. Scales
                from 0 (lossless) to 51 (worst). (default: None)
            verbose (`bool`, optional): Verbosity flag specifing if debug
                information should be printed.

        Attributes:
            pipe (sp.Popen): Direct access to the processing stream

        """
        self.path = path

        command = [ FFMPEG_BIN,
            '-y', # (optional) overwrite output file if it exists
            '-f', 'rawvideo',
            '-vcodec','rawvideo',
            '-s', str(width)+'x'+str(height), # size of one frame
            '-pix_fmt', 'bgr24',
            '-r', str(fps), # frames per second
            '-i', '-', # The imput comes from a pipe
            '-vcodec', codec,
            '-preset', preset,
            ]
        if lossless:
            command.extend(['-crf','0'])
        elif crf:
            command.extend(['-crf',str(crf)])
        command.append(path)

        if verbose: print("COMMAND: ", command)
        pipe_err = None if verbose else open(os.devnull, 'w')
        self.pipe = sp.Popen(command, stdin = sp.PIPE, bufsize=10**8, stderr=pipe_err, stdout=pipe_err)

    def write(self, arr):
        """Write a new image to the stream.

        Args:
            arr (np.array): The image to add to the video stream.

        Returns:
            None

        """

        arr = np.uint8(arr)
        self.pipe.stdin.write( arr.tostring() )
        self.pipe.stdin.flush()

    def release(self):
        """Release the FFWriter.

        Kills the process and dumps the buffer.

        Returns:
            None

        """

        if self.pipe:
            self.pipe.stdin.close()
            if self.pipe.stderr is not None:
                self.pipe.stderr.close()
            self.pipe.wait()

        self.pipe = None

    def close(self):
        """Alias for `release()`.

        See Also:
            release()

        Returns:
            None

        """

        self.release()

    # Support the Context Manager protocol, to ensure that resources are cleaned up.
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()



#
# ''' TEST CASES '''
#
# def test_read():
#
#     #ff = FFReader('/home/amini/Downloads/VID_20170911_113925.mp4')
#     ff = FFReader('./test1000.h264',verbose=True)
#     fw = FFWriter('out.avi',1208,1920,codec="libx264",preset="ultrafast",crf=18)
#
#
#     #ff.seek(100)
#     import cv2 # cv2 just for displaying the images
#     for i in range(6000):
#         (ret, image) = ff.read()
#
#         if ret:
#             cv2.imshow('x',image)
#             cv2.waitKey(1)
#             fw.write(image)
#     fw.release()
#     ff.release()
#
#
# def test_lossless(**kwargs):
#     NFRAMES = int(1e2)
#     fread = FFReader('/sandbox/data/traces/camera_front.avi')
#     true = np.zeros((NFRAMES,fread.width,fread.height,3), dtype=np.uint8)
#     ff = FFWriter('out.avi',fread.width,fread.height, **kwargs)
#     #ff2 = FFWriter('out2.avi',fread.width,fread.height, **kwargs)
#     for i in range(NFRAMES):
#         #true[i] = np.uint8(fread.read())
#         (ret, img) = fread.read()
#         if ret:
#             true[i] = img
#             ff.write(true[i])
#     ff.release()
#     #ff2.release()
#
#     #read the written file to make check loss
#     ff = FFReader('out.avi',verbose=True)
#     err = 0
#
#     import cv2 # cv2 just for displaying the images
#     for i in range(0,NFRAMES):
#         ret, img = ff.read()
#         if not ret:
#             continue
#         img = img.astype(np.float)
#         #img = np.array(img, dtype=np.float)
#         exp = np.array(true[i], dtype=np.float)
#         bad = img-true[i]
#         err += abs(np.sum(bad))
#         cv2.imshow('loss',bad/255.)
#         cv2.waitKey(1000/30)
#     print "Total pixel loss:", err
#     ff.release()
#
# # test_read()
# #test_lossless() #true_lossless
# #test_lossless(codec='libx264') #true_lossless
# #test_lossless(crf=18) #true_lossless
