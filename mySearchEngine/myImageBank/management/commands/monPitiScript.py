from myImageBank.models import MyImageURL
from myImageBank.serializers import MyImageURLSerializer

myImage = MyImageURL(myUrl='https://image.freepik.com/vecteurs-libre/poisson_53876-59060.jpg')
myImage.save()
myImage = MyImageURL(myUrl='https://image.freepik.com/photos-gratuite/poisson-frais-blanc_144627-24519.jpg')
myImage.save()