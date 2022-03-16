# The website initial data

This folder contains all the data initially gathered to initialize our models. This data
is sourced below in case it was provided by a third-party and not generated in-house.

## Files

### hafsData_v18.json

The hafs mushaf in JSON format as is fetched from [King Fahd Glorious Qur'an Printing Complex](https://qurancomplex.gov.sa/techquran/dev/) as of 03/16/2022.

#### Data README

**KFGQPC Hafs Uthmanic Data**
Version: 0.18
Date: 2021-10-25
Update: 10.0

```
- Modify word (كلا) with (Alif Madd) to display properly at most software and devices
- Adding non-breaking space before aya mark for aya_text column
- Adding non-breaking space after jozz/hizb symbol for aya_text column
- Adding Ayamark Symbol to HTML file to appear ayamark properly
- Fix Shapes with final (ي) not rendering properly with Adobe products, such as Sura Al-Baqarah(2), Aya(18)
- Modify some Jozz numbers in data files such as Sura An-Naml(27) Aya(56-59) from (19) to (20)
- Modifying Encoding of "hafsData_v17.csv" file from UTF-8 to UTF-8-BOM
- Modifying Word (فادارأتم) sura Al-Baqarah(2) aya(72) to display properly on different platforms
- Removing Kashida from different places in aya_text_emlaey column
- Modifying Aya(285) in Sura Al-Baqarah(2) in aya_text column at hafsData_v18.html file
```

It includes two folders:

1. Uthmanic Hafs Ver18 font: It contains font file and whole Qur'an data in MS document file
1. Uthmanic Hafs Ver18 data: It contains files for developers.

**Columns:**

```
- id (int):               Auto_increment Number
- jozz (int):             Jozz Number
- sora_no (int):          Sora Number
- sora_name_en (varchar): Sora Name in English
- sora_name_ar (varchar): Sora Name in Arabic (UthmanicHafs ttf font file)
- page (int):             Page Number
- line_start (int):       Start Line of Aya
- line_end (int):         End Line of Aya
- aya_no (int):           Aya Number
- aya_text (text):        Text of the Aya  in UthmanicHafs ttf font file
- aya_text_emlaey (text): Emlaey Text of the Aya used for search purpose
```

### hafsData_clean_arabic_sura_v18
We've added this file to not manipulate the data fetched KFGQPC. It includes a mapping
of the values in `sora_name_ar` in hafsData_v18.json to a clean value that doesn't
include diacritics.
