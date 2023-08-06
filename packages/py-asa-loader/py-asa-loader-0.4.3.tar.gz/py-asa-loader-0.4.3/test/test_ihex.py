import conftest
from asaloader.ihex import parseIHex, resize_to_page, cut_to_pages

a = parseIHex('test/test4.hex')


# a = [
#     {
#         'address': 5,
#         'data': b'123456'
#     }
# ]

b = resize_to_page(a, 256)

c = cut_to_pages(b, 256)

print(a)
print(b)
print(c)

print(len(a[0]['data']))
print(len(a[1]['data']))

print(len(b[0]['data']))

