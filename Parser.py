class ParserMethod :
    """
    File parsing macros.
    """
    
    def __init__(self) :
        """
        Initializes necessary variables for the class.
        """
    def Parse(self, parse_object, key1, key2) :
        """
        This function extracts a desired section from an input file that has
        been prepared through Tools.IO
              
        Arguments:
            <parse_object> specifies object to be parsed (variable).
            <key1> identifies start of section to be parsed (string).
            <key2> identifies end of section to be parsed (string).
            
        Return: List
            
        Keys 1 and 2 delimit the boundaries of the section to be parsed. These need
        to be coded into the source file as well so that the file to be parsed
        contains these keys.
        """
        self.parsed = [];
        self.start_key = key1;
        self.stop_key = key2;
        self.start = 0;
        self.end = 0;
        
        self.indexed_file = parse_object;
        
        for i in range(0, len(self.indexed_file)) : # Delimit parse section
            if self.indexed_file[i] == self.start_key :
                self.start = i;
            elif self.indexed_file[i] == self.stop_key :
                self.end = i;

        for i in range((self.start) + 1, (self.end)) : # Parse section
            self.parsed = self.parsed + [self.indexed_file[i]];
            
        return self.parsed

    def ColumnExtract(self, extract_object, column):
        """
        This function extracts the desired column of a table extracted from an 
        input file treated with Tools.IO. File must be in string format. Columns
        are not required to have fixed widths and properly formatted so long as
        they are separated by at least 1 blank space. IMPORTANT: elements of each
        column must be a continuous string of literals WITHOUT spaces.
        
        Arguments:
            <extract_object> specifies desired object from which a column is 
            extracted.
            <column> specifies the desired column to be extracted (integer).
            
        Return: List
        """
        
        self.column_extract = [];
        self.extract_object = extract_object;

        for i in range(0, len(self.extract_object)) :
            self.k = 0; # Column counter
            self.toggle = 0; # Used to toggle k counter
            self.string = ""; # String to hold energy value
            for j in range (0, len(self.extract_object[i])) :
                if ((self.extract_object[i][j] != " " ) 
                    and (self.extract_object[i][j] != "\t")) : 
                        if (self.toggle == 0) : 
                        # Recognizes start of a column
                            self.k = self.k + 1;
                            self.toggle = 1;
                if ((self.extract_object[i][j] == " ") 
                    or (self.extract_object[i][j] == "\t")) :
                        if (self.toggle == 1) :
                        # Recognizes end of a column
                            self.toggle = 0; 
                if (self.k == column) and (self.toggle == 1) : 
                # Construct Energy value as a string
                    self.string = self.string + self.extract_object[i][j]; 
            self.column_extract = self.column_extract + [self.string];
            
        return self.column_extract