import gzip


class BaseGzip(object):

    def __init__(self, bufsize, fin=None, fout=None):
        self.bufsize = bufsize
        self.fout = fout

    def compress(self, src, dst):
        """
        压缩文件
        :param src:
        :param dst:
        :return:
        """
        self.fin = open(src, 'rb')
        self.fout = gzip.open(dst, 'wb')

        self.__in2out()

    def decompress(self, gzFile, dst):
        """
        解压文件
        :param gzFile:
        :param dst:
        :return:
        """
        self.fin = gzip.open(gzFile, 'rb')
        self.fout = open(dst, 'wb')

        self.__in2out()

    def __in2out(self):
        while True:
            buf = self.fin.read(self.bufsize)
            if len(buf) < 1:
                break
            self.fout.write(buf)

        self.fin.close()
        self.fout.close()


