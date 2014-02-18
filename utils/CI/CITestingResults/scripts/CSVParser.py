import csv

class CSVParser(object):
    """docstring for CSVParser"""
    def __init__(self, fileName, labels, rows_to_jump):
        self.fileName = fileName
        self.labels = labels
        self.ROWS_TO_JUMP = rows_to_jump
        self.prev_info = []
        self.info = []

        self._preprocess()
        
    def _preprocess(self):
        """ 
        This method preprocess the CSV file in order to separate the additional info 
        included from the CSV stream itself
        """
        f = open(self.fileName, 'rb')

        i = 0
        for row in f.readlines():
            if (i < self.ROWS_TO_JUMP):
                self.prev_info.append(row)
            i += 1
        f.close()

        f = open(self.fileName, 'rb')
        reader = csv.DictReader(f, self.labels)

        # print "=============================\n"
        # for row in reader:
        #     print row
        # print "=============================\n"

        # Cast to an array of dictionaries and remove prev info data
        self.info = [row for row in reader][self.ROWS_TO_JUMP:]

    def filterColumns(self, filterLabels):
        """
        This method filters the filterLabels' columns from the CSV

        @type filterLabels: List
        @param filterLabels: list of labels to filter.
        """

        for row in self.info:
            for key in row.keys():
                if key not in filterLabels:
                    del row[key]

        #
        # Remove the labels to be filtered to the original label list, so that
        # we get clean data to write 
        #
        self.labels = [label for label in self.labels if label in filterLabels]

    def filterRows(self, condition):
        """
        This method filters the CSV rows contained in self.info, according
        to the given condition.

        This version only allows to filter rows upon two kind of conditions:
            1. Over integers/floats, e.g. 3 > 0. 
            2. Equality over strings, e.g. "b2g.CONTACTS == b2g.CONTACTS".

        Examples:
            parser.filterRows({"VERSION": "v1.2"}): get only the rows where the
            VERSION field is equal to "v1.2"

            parser.filterRows({"BUILD_NUMBER": ">20"}): get only the rows where
            the BUILD_NUMBER field is greater than 20
 
        @type condition: dictionary (key: "Label to apply the condition, value: the condition itself)
        @param condition: the condition to filter the CSV file
        """
        #
        # This is gonna be the array where the matching rows are pushed
        #
        _new_info = []
        for row in self.info[1:]: #skip first row (the labels)
            for data_key, data_value in row.items():
                for filter_key, filter_value in condition.items(): 
                    if filter_key == data_key:
                        try:
                            int(data_value)
                        except ValueError:
                            try:
                                float(data_value)
                            except ValueError:
                                #
                                # if we arrive here, assume it is a string condition
                                #
                                if cmp(data_value, filter_value) == 0:
                                    _new_info.append(row)
                                continue
                        #
                        # Number expression (3 > 0). We have to evaluate it.
                        #
                        expression = data_value + filter_value
                        if eval(expression):
                            _new_info.append(row)

        #
        # Do not forget to add the labels row to the filtered info
        #
        _new_info.insert(0, self.info[0])
        self.info = _new_info


    def write(self, path_to_file):
        """
        This method dumps the processed data into another CSV file.

        @type path_to_file: string
        @parama path_to_file: the path where the new brand CSV will be generated.
        """
        file = open(path_to_file, "wb")
        writer = csv.writer(file)

        #
        # Dump previous data
        #
        for item in self.prev_info:
            writer.writerow([item])
        file.close()

        #
        # Dump filtered data
        #
        file = open(path_to_file, "ab")
        dWriter = csv.DictWriter(file, fieldnames=self.labels)
        for item in self.info:
            dWriter.writerow(item)
        file.close()
        

    def __str__(self):
        s = "------ Prev info -------\n"
        for item in self.prev_info:
            s += item + "\n"

        s += "------ Labels ------\n"
        for item in self.labels:
            s += item + ", "
        s += "\n"
        s += "------ CSV info -------\n"

        for row in self.info:
            for key, value in row.items():
                s += value + ", "
            s += "\n"
        return s


