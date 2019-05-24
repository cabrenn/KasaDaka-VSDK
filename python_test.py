import wave
import io

ROOT = "d:\ict4d_sounds\\new\\"

infiles = ["{}are_you_satisfied.wav".format(ROOT), "{}enter_days.wav".format(ROOT)]
outfile = "{}sounds.wav".format(ROOT)
"""
data= []

for infile in infiles:
    w = wave.open(infile, 'rb')
    data.append( [w.getparams(), w.readframes(w.getnframes())] )
    w.close()
"""
urls = [
    'http://django-static.ict4d.kasadaka.com/2019_group_12/django/5_en.wav',
    'http://django-static.ict4d.kasadaka.com/2019_group_12/django/bags_of.wav',
    'http://django-static.ict4d.kasadaka.com/2019_group_12/django/rice_1Y6PeFb.wav'
]




import wave
import io
import requests

data = []

for url in urls:
    r = requests.get(url)
    w = wave.open(io.BytesIO(r.content), 'rb')
    data.append( [w.getparams(), w.readframes(w.getnframes())] )
    w.close()

a = io.BytesIO()
output = wave.open(a, 'wb')
#output = wave.open(outfile, 'wb')
output.setparams(data[0][0])

for sound in data:
    output.writeframes(sound[1])

output.close()
a.seek(0)
print(a.getvalue())

"""
output.setparams(data[0][0])
output.writeframes(data[0][1])
output.writeframes(data[1][1])
output.close()
a.flush()
a.getvalue()
a.close()

"""