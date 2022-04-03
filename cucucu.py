doska = [['lB', 'kB', 'cB', 'fB', 'gB', 'cB', 'kB', 'lB'],
         ['pB', 'pB', 'pB', 'pB', 'pB', 'pB', 'pB', 'pB'],
         ['_', '_', '_', '_', '_', '_', '_', '_'],
         ['_', '_', '_', '_', '_', '_', '_', '_'],
         ['_', '_', '_', '_', '_', '_', '_', '_'],
         ['_', '_', '_', '_', '_', '_', '_', '_'],
         ['pW', 'pW', 'pW', 'pW', 'pW', 'pW', 'pW', 'pW'],
         ['lB', 'kB', 'cB', 'fB', 'gB', 'cB', 'kB', 'lB']]

result = ""
for i in doska:
    for j in i:
        result += j + ","

print(result)
