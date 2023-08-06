from neon_goby.clean import clean
from neon_goby.split import split

class NeonGoby(object):
  @staticmethod
  def clean(text, anonymous=True):
    return clean(text, anonymous=anonymous)

  @staticmethod
  def split(text, anonymous=True):
    return split(text)

  @staticmethod
  def parse(text, anonymous=True):
    return split(clean(text, anonymous=anonymous))
