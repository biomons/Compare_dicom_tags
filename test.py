from compare_dicom_tags import compare_dicom_tags

inst = compare_dicom_tags()
inst.compare_datasets('RP11.dcm', 'RP11b.dcm', diff_only=False)
