import fnmatch
import os
import arcpy
import pandas as pd
from metaphone import doublemetaphone
from enum import Enum
from collections import defaultdict
import re

class pathFinder:


    def __init__(self, env_0=None, env_1=None, outPathFolder=None, outPathGDB = None):
        self.env_0 = env_0
        self.env_1 = env_1
        self.outPathFolder = outPathFolder
        self.outPathGDB = outPathGDB




    def get_path_for_all_feature_from_gdb(self, type ="Polygon"):
        gdbPath =[]
        for dirpath, dirnames, filenames in arcpy.da.Walk(self.env_0, datatype="FeatureClass", type=type):
            for filename in filenames:
                gdbPath.append(os.path.join(dirpath, filename))

        return list(gdbPath)

    def get_file_path_with_wildcard_from_gdb(self, wildcard=None, type="Polygon"):
        gdbPath = []

        if wildcard is not None:


            for dirpath, dirnames, filenames in arcpy.da.Walk(self.env_0, datatype="FeatureClass", type=type):
                for filename in fnmatch.filter(filenames, wildcard):
                    gdbPath.append(os.path.join(dirpath, filename))
            print("\nfound {} many file(s)".format(len(gdbPath)))

        return list(gdbPath)



    @classmethod
    def get_shapefile_path_walk(cls, path):
        file_loc = []

        # use os.walk to find the root, directory, and files
        for root, dirs, files in os.walk(path):
            # create a loop by files
            for file in files:
                # for the files that endswith .shp, join the root and file
                if file.endswith(".shp"):
                    # create a local variable that we can assign the root and file path then loop it
                    path = os.path.join(root, file)
                    # append the path in our file_loc list
                    file_loc.append(path)

        return list(file_loc)


    @classmethod
    def get_shapefile_path_wildcard(cls, path, wildcard):
        file_loc = []

        # use os.walk to find the root, directory, and files
        for root, dirs, files in os.walk(path):
            # create a loop by files
            for file in fnmatch.filter(files, wildcard+".shp"):
                # for the files that endswith .shp, join the root and file
                file_loc.append(os.path.join(root, file))

        if list(file_loc) == 'NoneType':
            raise Warning("Did not find path, check your wild card")

        else:
            return list(file_loc)

    @classmethod
    # create a list of fips from the table.
    def make_fips_list(cls):
        import pandas as pd
        Fips_table_path = r"D:\FCC_GIS_Projects\MFII\csv\state FiPS.txt"
        data = pd.read_csv(Fips_table_path, sep='|')
        data["STATE"] = data["STATE"].astype(str)
        data['STATE'] = data["STATE"].apply(lambda x: x.zfill(2))
        return data.STATE.tolist()


    @classmethod
    def query_provider_by_FIPS(cls, path, fips):
        import pandas as pd
        df = pd.read_csv(path)
        fips_query = df.query("stateFIPS ==" + str(fips))
        fips_query = fips_query.dropna(axis=1, how="any")
        return list(fips_query.applymap(int).values.flatten()[1:])

    @classmethod
    def query_provider_pid_by_provider_FRN(cls, table_path, frn):
        df = pd.read_csv(table_path)
        df['f477_provider_frn'] = df["f477_provider_frn"].apply(lambda x: "%010d" % x)
        query_results = df.query("f477_provider_frn == '{}'".format(frn))
        #print(query_results)
        dic = query_results.to_dict('records')
        return dic[0]

    @classmethod
    def query_pid_by_dba(cls, table_path, dba):

        df = pd.read_csv(table_path)
        # print(df)
        query_results = df.query("dba =='{}'".format(dba))
        dic = query_results.to_dict('records')
        #print(dic)
        return dic[0]

    @classmethod
    def extract_dba(cls, fc_input, field_name_list):

        return list(set([row[0] for row in arcpy.da.SearchCursor(fc_input, field_name_list)]))[0]



    @classmethod
    def query_pid_by_state_fips(cls, table_path=r"D:\FCC_GIS_Projects\jon\cetc_subsidy-pid_spin_sac_fhcs_amount-with_territories-sep2017-19jun2018.csv", state_fips=None):

        df = pd.read_csv(table_path)
        # print(df)
        query_results = df.query("cetc_state_fips =='{}'".format(state_fips))
        dic = query_results.to_dict('records')
        # print(dic)
        return dic

    @classmethod
    def filter_List_of_shapefiles_paths_with_wildcard(cls, path_link_list, wildcard):
        for path_link in path_link_list:
            if fnmatch.fnmatch(os.path.basename(path_link), wildcard + ".shp"):
                return path_link



    @classmethod
    def filter_List_of_featureclass_paths_with_wildcard(cls, path_link_list, wildcard):
        sorted_list = []
        for path_link in path_link_list:
            if fnmatch.fnmatch(os.path.basename(path_link), wildcard):
                sorted_list.append(path_link)
        print("found {} number of files".format(len(sorted_list)))
        return list(sorted_list)


    @classmethod
    def get_shapefile_path_walk_dict(cls, path):


        file_dict = defaultdict(list)

        # use os.walk to find the root, directory, and files
        for root, dirs, files in os.walk(path):
            # create a loop by files
            for file in files:
                # for the files that endswith .shp, join the root and file
                if file.endswith(".shp"):
                    # create a local variable that we can assign the root and file path then loop it
                    file_dict[root].append(file)


        return file_dict

    def create_number_provider_per_state(self, regex = r"T(?P<state>\d{1,2})_(?P<pid>\d{1,2})(?P<cetc_sac>\w+)?", table_outpu=None):
        from collections import defaultdict

        fc_list = self.get_path_for_all_feature_from_gdb()

        file_path_dict = defaultdict(list)

        for x in fc_list:
            file_path_dict[os.path.dirname(x)].append(os.path.basename(x))


        #complete_dict = defaultdict(list)
        #for key, values in file_path_dict.items():
        #    for x in values:

        #        regex = regex
        #        regex_dict = re.search(regex, x).groupdict()
        #        complete_dict[regex_dict['state']].append(regex_dict["pid"])


        return file_path_dict


    @classmethod
    def get_number_of_provider_from_attribute_table(cls,in_feature, field):

        values = [row[0] for row in arcpy.da.SearchCursor(in_feature, field)]

        return set(values)

    @classmethod
    def findField(cls, fc, field):
        fieldnames = [field.name for field in arcpy.ListFields(fc)]
        if field in fieldnames:
            return field
        else:
            return "pass"


    @classmethod
    def make_list_from_filename(cls, inlist,
                                regex = r"^dagg_(?P<state>\d{1,2})_(?P<pid>\d{1,3})_(?P<pname>\w.+)_subsidized.+$"):

        def check_key(dt, key):
            if key in dt:
                #print("key exits")
                return True
            else:
                return False

        complete_dict = defaultdict(set)

        key = 0
        for name in inlist:

            regex_dict = re.search(regex, os.path.basename(name)).groupdict()
            #print(regex_dict)

            if check_key(regex_dict, 'pid'):
                complete_dict[name].add((regex_dict["pname"],regex_dict['pid']))
            else:
                complete_dict[name].add(regex_dict['pname'])

                key +=1

        return dict(complete_dict)



    class Threshold(Enum):
        WEAK = 0
        NORMAL = 1
        STRONG = 2

    def double_metaphone(self, value):
        #print(doublemetaphone(value))
        return doublemetaphone(value)

    #(Primary Key = Primary Key) = Strongest Match
    #(Secondary Key = Primary Key) = Normal Match
    #(Primary Key = Secondary Key) = Normal Match
    #(Alternate Key = Alternate Key) = Minimal Match

    def double_metaphone_compare(self, tuple1,tuple2,threshold):
        if threshold == self.Threshold.WEAK:
            if tuple1[1] == tuple2[1]:
                return True
        elif threshold == self.Threshold.NORMAL:
            if tuple1[0] == tuple2[1] or tuple1[1] == tuple2[0]:
                return True
        else:
            if tuple1[0] == tuple2[0]:
                return True
        return False


    def check_names_return_tuple_list(self, reference_dict, match_dict):
            from fuzzywuzzy import fuzz

            match = defaultdict(set)

            for k, v in reference_dict.items():

                for kk, vv in match_dict.items():

                    #print("\n\nreference name")
                    reference_name = list(v)[0].lower()
                    #print(reference_name)


                    #print("Names to be compared")
                    match_names = list(vv)[0].lower()
                    #print(match_names)


                    #0 = less than 70
                    #1 = ">=90"
                    #2 = ">=85 and <90"
                    #3 = ">=70 and <80"

                    token_score = fuzz.token_sort_ratio(reference_name, match_names)

                    if token_score>=90:
                        print("the names match strong")
                        match[1].add((k, kk, token_score))
                    elif token_score>=85 and token_score<90:
                        match[2].add((k, kk, token_score))

                    elif token_score>=75 and token_score<85:
                        match[3].add((k, kk, token_score))

                    else:
                        match[0].add((k, kk, token_score))

            return match

    def check_names_return_tuple_list_dont_use(self, reference_dict, match_dict):


            match = defaultdict(set)

            for k, v in reference_dict.items():

                for kk, vv in match_dict.items():

                    #print("\n\nreference name")
                    reference_name = list(v)[0].strip("_")
                    #print(reference_name)
                    tp1 = self.double_metaphone(reference_name)

                    #print("Names to be compared")
                    match_names = list(vv)[0].strip("_")
                    #print(match_names)
                    tp2 = self.double_metaphone(match_names)

                    if self.double_metaphone_compare(tp1, tp2, self.Threshold.STRONG):
                        print("the names match strong")
                        match[self.Threshold.STRONG].add((k, kk))
                    elif self.double_metaphone_compare(tp1, tp2, self.Threshold.NORMAL):
                        print("the names match normal")
                        match[self.Threshold.NORMAL].add((k, kk))


                    elif self.double_metaphone_compare(tp1, tp2, self.Threshold.WEAK):
                        print("the names match weak")
                        match[self.Threshold.WEAK].add((k, kk))




                    else:
                        continue

            return match
