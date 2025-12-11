from pydicom import dcmread, dataelem, multival, config
import pydicom

#
# written by René Monshouwer ( Rene.monshouwer@radboudumc.nl)
# primary goal to compare rtplan files

class compare_dicom_tags:

    tagdatalist = []

    class tagdata():
        #contains tag data and additional information like nested level and 'parents'
        def __init__(self, value, tag, keyword, level, levelnames, levelcounter):
            self.value = value
            self.level = level
            self.tag = tag
            self.keyword = keyword
            self.levelnames = levelnames.copy()
            self.levelcounter = levelcounter
            self.refvalue = ''

        # for when you print  tagdata
        def __str__(self):
            if len(str(self.value)) < 50:
                mystr = "{} {:50} {:25} {:40} {}".format(self.level, str(self.levelnames), str(self.levelcounter),
                                                       str(self.keyword), str(self.value))
            else:
                mystr = "{} {:50} {:25} {:40} {:80}".format(self.level, str(self.levelnames), str(self.levelcounter),
                                                         str(self.keyword), str(self.value))
            return mystr

    def scan_dataset(self, dataset,level, inputlevelnames, levelcounters):
        # main routine that gets recursively called when going through a nested list of tags

        # Note: the lists and dicts are passed by reference and should thus be copied otherwise recursion does not work
        levelnames_local = inputlevelnames.copy()
        levelcounters_local = levelcounters.copy()

        for tag in dataset:
            if tag.VR != 'SQ':
                self.tagdatalist.append(self.tagdata(tag.value, tag.tag, tag.keyword,
                                                     level, levelnames_local, levelcounters_local))
            else:
                levelnames_local.append(tag.tag)
                nested_counter = 0
                for dataset2 in tag:
                    levelcounters_local[level] = nested_counter
                    nested_counter = nested_counter+1
                    self.scan_dataset(dataset2, level+1, inputlevelnames=levelnames_local,
                                      levelcounters=levelcounters_local)
                levelnames_local = inputlevelnames.copy()
                levelcounters_local = levelcounters.copy()

    def get_tagvalue(self, ds_ref, tag):
        # to get metching tag from reference dataset ds_ref
        # extra information about the tag is contained in the variable tag which should be of type : tagdata
        refval = dataelem
        refval.value = '\033[91mNot Found\033[0m'

        if tag.level > 4:
            refval.value = '\033[91mTag level above 4 not implemented\033[0m'
            return refval
        if tag.level == 0:
            if tag.tag in ds_ref:
                refval = (ds_ref[tag.tag])
        try:
            if tag.level == 1:
                refval = (ds_ref[tag.levelnames[0]][tag.levelcounter[0]][tag.tag])
            elif tag.level == 2:
                refval = (ds_ref
                          [tag.levelnames[0]][tag.levelcounter[0]]
                          [tag.levelnames[1]][tag.levelcounter[1]][tag.tag])
            elif tag.level == 3:
                refval = (ds_ref
                          [tag.levelnames[0]][tag.levelcounter[0]]
                          [tag.levelnames[1]][tag.levelcounter[1]]
                          [tag.levelnames[2]][tag.levelcounter[2]][tag.tag])
            elif tag.level == 4:
                refval = (ds_ref
                          [tag.levelnames[0]][tag.levelcounter[0]]
                          [tag.levelnames[1]][tag.levelcounter[1]]
                          [tag.levelnames[2]][tag.levelcounter[2]]
                          [tag.levelnames[3]][tag.levelcounter[3]][tag.tag])
        except:
            #print('exception encountered'+str(tag_level))
            pass
        return refval

    def print_comparison(self, ds1, ds2, diff_only=False):
        # rows are red when the values disagree or when matching data is not found

        self.scan_dataset(ds1, 0, inputlevelnames=[], levelcounters={})
        for td in self.tagdatalist:
            refval = self.get_tagvalue(ds2, td)
            td.refvalue = refval.value
            if refval.value != td.value:
                if type(td.value) == pydicom.multival.MultiValue:
                    if (len(td.value)) > 10:
                        print('\033[91m{:<115} \033[0m'.format(str(td)))
                        print(
                            '\033[91m{: <120s}{} \033[0m'.format("", str(refval.value)))
                    else:
                        print('\033[91m{:<175} {}\033[0m'.format(str(td), str(refval.value)))
                else:
                    print('\033[91m{:<175} {}\033[0m'.format(str(td), str(refval.value)))
            else:
                if not diff_only:
                    print('{:<175} {}'.format(str(td), str(refval.value)))

    def compare_datasets(self, ds1, ds2, metadata=True, diff_only=False, ignore_validation=True):
        # compares two datasets and pretty prints
        # ds1 and ds2 are either strings and then assumed to be filenames, or pydicom datasets

        if ignore_validation:
            pydicom.config.settings.reading_validation_mode = 0  # ignore reading errors

        if isinstance(ds1, str):
            filename1 = ds1
            ds1 = dcmread(filename1)
            print('File1: (left column)  :' + filename1)

        if isinstance(ds2, str):
            filename1 = ds2
            ds2 = dcmread(filename1)
            print('File2: (right column)  :' + filename1)

        if metadata:
            print('\n\n-----------metadata---------------')
            self.print_comparison(ds1.file_meta, ds2.file_meta, diff_only=diff_only)

        print('\n\n-----------tag data---------------')
        self.print_comparison(ds1, ds2, diff_only=diff_only)
