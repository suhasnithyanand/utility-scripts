from usps import USPSApi, Address

address = Address(
    name='Suhas Nithyanandappa',
    address_1='60 Vinatge Circle, Apt 307',
    city='Pleasanton',
    state='CA',
    zipcode='94566'
)

# address = Address(
#     name='Gate 6, 1600 Marietta Rd NW',
#     address_1='SP Richards CO DC, 190 Selig Drive',
#     city='Atlanta',
#     state='GA',
#     zipcode='30336'
# )
usps = USPSApi('321BLUME7569', test=True)
validation = usps.validate_address(address)
print(validation.result)


