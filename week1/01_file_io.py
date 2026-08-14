with open("D:/github_repos/caspel/week1/output/history.txt", "a", encoding="utf-8") as file:
    file.write("Yeni request daxil oldu\n") # nə qədər run olunsa, faylın sonuna o qədər dəfə append edir

with open("output/history.txt", "w", encoding="utf-8") as file:
    file.write("Burası faylın yeni məzmunudur.") # faylı yeniləyir və əvvəlki məlumatları silir

with open("output/history.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content) # faylı oxuyur və ekrana yazdırır