# Compare_dicom_tags
Compares the tags of two dicom tags and highlights differences

Mainly developed for comparing RTPLAN dicom files

example :

```
from compare_dicom_tags import compare_dicom_tags

inst = compare_dicom_tags()
inst.compare_datasets('RP11.dcm', 'RP11b.dcm', diff_only=False)
```

Column description:
- depth : tag codes in right brackets []
- index of the items in case of a (nested) sequence 
- name/description of the item
- value of item in the first file
- value of item in the second file

A line is printed in red when a differerence is detected  
setting **diff_only=True** prints only differences

example output:
```
0 []                                                 {0: 0}                    RTPlanDescription                                                                                Not Found
0 []                                                 {0: 0}                    RTPlanDate                               20250317                                                20250317
0 []                                                 {0: 0}                    RTPlanTime                               082128                                                  135438
0 []                                                 {0: 0}                    RTPlanGeometry                           PATIENT                                                 PATIENT
1 [(300a, 0070)]                                     {0: 0, 1: 0}              FractionGroupNumber                      1                                                       1
1 [(300a, 0070)]                                     {0: 0, 1: 0}              NumberOfFractionsPlanned                 1                                                       1
1 [(300a, 0070)]                                     {0: 0, 1: 0}              NumberOfBeams                            1                                                       1
1 [(300a, 0070)]                                     {0: 0, 1: 0}              NumberOfBrachyApplicationSetups          0                                                       0
2 [(300a, 0070), (300c, 0004)]                       {0: 0, 1: 0}              BeamDoseSpecificationPoint               [10.0, 100.0, 280.0]                                    [10, 100, 280]
2 [(300a, 0070), (300c, 0004)]                       {0: 0, 1: 0}              BeamDose                                 0.9511360000000001                                      0.951136
```
So for the last row above, there is one nested sequence, and both have index 0 (so are the first item of the sequence )
