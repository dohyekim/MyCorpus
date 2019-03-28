with open("chart", "w", encoding="utf-8") as chartfile:
    chartfile.write("D1 ,K1 ,E1  ,\n")
for i in range(2,145):
    with open("chart", "a", encoding="utf-8") as addfile:
        addfile.write("D{},K{},E{}, \n".format(i,i,i))
# a = []
# with open("chart","r",encoding="utf-8") as readfile:
#     for line in readfile:
#         a.append(line[1])
#     print(len(a))


    # print(len(readfile))
    # print(len(readfile[-1]))
