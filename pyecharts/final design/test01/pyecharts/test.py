from clinicaltrial.models import Clinicaltrial

Clinicaltrial.objects.filter(for_anzsrc_categories__contains="01 Mathematical Sciences").count()
# Clinicaltrial.objects.filter(for_anzsrc_categories="01 Mathematical Sciences").count()




list = (
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="01 Mathematical Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0102 Applied Mathematics").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0103 Numerical and Computational Mathematics").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0104 Statistics").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="02 Physical Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0202 Atomic, Molecular, Nuclear, Particle and Plasma Physics").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0204 Condensed Matter Physics").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0205 Optical Physics").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0299 Other Physical Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="03 Chemical Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0301 Analytical Chemistry").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0305 Organic Chemistry").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="04 Earth Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0402 Geochemistry").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="05 Environmental Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0502 Environmental Science and Management").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="06 Biological Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0601 Biochemistry and Cell Biology").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0602 Ecology").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0603 Evolutionary Biology").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0604 Genetics").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0605 Microbiology").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0606 Physiology").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0607 Plant Biology").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="07 Agricultural and Veterinary Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0703 Crop and Pasture Production").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0707 Veterinary Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="08 Information and Computing Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0801 Artificial Intelligence and Image Processing").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="09 Engineering").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0903 Biomedical Engineering").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0905 Civil Engineering").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0911 Maritime Engineering").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0912 Materials Engineering").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="0915 Interdisciplinary Engineering").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="10 Technology").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1004 Medical Biotechnology").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1005 Communications Technologies").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="11 Medical and Health Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1102 Cardiorespiratory Medicine and Haematology").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1103 Clinical Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1104 Complementary and Alternative Medicine").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1106 Human Movement and Sports Science").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1108 Medical Microbiology").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1109 Neurosciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1110 Nursing").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1111 Nutrition and Dietetics").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1112 Oncology and Carcinogenesis").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1113 Ophthalmology and Optometry").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1114 Paediatrics and Reproductive Medicine").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1115 Pharmacology and Pharmaceutical Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1117 Public Health and Health Services").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1199 Other Medical and Health Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="13 Education").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1302 Curriculum and Pedagogy").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1303 Specialist Studies In Educationv").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="14 Economics").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1402 Applied Economics").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="15 Commerce, Management, Tourism and Services").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1503 Business and Management").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1505 Marketing").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="16 Studies in Human Society").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1604 Human Geography").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1605 Policy and Administration").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1606 Political Science").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1608 Sociology").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="17 Psychology and Cognitive Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1701 Psychology").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1702 Cognitive Sciences").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="18 Law and Legal Studies").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1801 Law").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="19 Studies in Creative Arts and Writing").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1902 Film, Television and Digital Media").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="1904 Performing Arts and Creative Writing").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="20 Language, Communication and Culture").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="2002 Cultural Studies").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="2004 Linguistics").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="21 History and Archaeology").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="2103 Historical Studies").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="22 Philosophy and Religious Studies").count(),
Clinicaltrial.objects.filter(for_anzsrc_categories__contains="2203 Philosophy").count()
)

list_name = ["01 Mathematical Sciences:",
        "0102 Applied Mathematics",
        "0103 Numerical and Computational Mathematics",
        "0104 Statistics",
        "02 Physical Sciences",
        "0202 Atomic, Molecular, Nuclear, Particle and Plasma Physics",
        "0204 Condensed Matter Physics",
        "0205 Optical Physics",
        "0299 Other Physical Sciences",
        "03 Chemical Sciences",
        "0301 Analytical Chemistry",
        "0305 Organic Chemistry",
        "04 Earth Sciences",
        "0402 Geochemistry",
        "05 Environmental Sciences",
        "0502 Environmental Science and Management",
        "06 Biological Sciences",
        "0601 Biochemistry and Cell Biology",
        "0602 Ecology",
        "0603 Evolutionary Biology",
        "0604 Genetics",
        "0605 Microbiology",
        "0606 Physiology",
        "0607 Plant Biology",
        "07 Agricultural and Veterinary Sciences",
        "0703 Crop and Pasture Production",
        "0707 Veterinary Sciences",
        "08 Information and Computing Sciences",
        "0801 Artificial Intelligence and Image Processing",
        "09 Engineering",
        "0903 Biomedical Engineering",
        "0905 Civil Engineering",
        "0911 Maritime Engineering",
        "0912 Materials Engineering",
        "0915 Interdisciplinary Engineering",
        "10 Technology",
        "1004 Medical Biotechnology",
        "1005 Communications Technologies",
        "11 Medical and Health Sciences",
        "1102 Cardiorespiratory Medicine and Haematology",
        "1103 Clinical Sciences",
        "1104 Complementary and Alternative Medicine",
        "1106 Human Movement and Sports Science",
        "1108 Medical Microbiology",
        "1109 Neurosciences",
        "1110 Nursing",
        "1111 Nutrition and Dietetics",
        "1112 Oncology and Carcinogenesis",
        "1113 Ophthalmology and Optometry",
        "1114 Paediatrics and Reproductive Medicine",
        "1115 Pharmacology and Pharmaceutical Sciences",
        "1117 Public Health and Health Services",
        "1199 Other Medical and Health Sciences",
        "13 Education",
        "1302 Curriculum and Pedagogy",
        "1303 Specialist Studies In Education",
        "14 Economics",
        "1402 Applied Economics",
        "15 Commerce, Management, Tourism and Services",
        "1503 Business and Management",
        "1505 Marketing",
        "16 Studies in Human Society",
        "1604 Human Geography",
        "1605 Policy and Administration",
        "1606 Political Science",
        "1608 Sociology",
        "17 Psychology and Cognitive Sciences",
        "1701 Psychology",
        "1702 Cognitive Sciences",
        "18 Law and Legal Studies",
        "1801 Law",
        "19 Studies in Creative Arts and Writing",
        "1902 Film, Television and Digital Media",
        "1904 Performing Arts and Creative Writing",
        "20 Language, Communication and Culture",
        "2002 Cultural Studies",
        "2004 Linguistics",
        "21 History and Archaeology",
        "2103 Historical Studies",
        "22 Philosophy and Religious Studies",
        "2203 Philosophy"
        ]

for i in range(0,82):
    print("{}:".format(i),list[i])


list.sort()

print(list)