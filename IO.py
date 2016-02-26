class IOMethod :
    def __init__(self) :
        """
        Initializes necessary variables for the class.
        """

    def InMethod(self, path) :
        """
        This function reads a file and attempts to convert its contents into an
        array whose elements are individual lines of the file for ease of 
        manipulation.
        
        Arguments:
            <path> specifies path to source file (string).
        
        Return: List
        """
        self.indexed_file = [];
        
        self.input_file = open(path, 'r');
        for i in self.input_file : # Converts file to array
            self.indexed_file = self.indexed_file + [i.rstrip('\n')];

        self.input_file.close();
        
        return self.indexed_file
    
    def OutMethod(self, write_object, path, mode, delimit) :
        """
        This function attempts to convert an object to string format and appends
        it to the output file.
        
        Arguments:
            <write_object> specifies object to write to file (variable).
            <path> specifies path to output file (string).
            <mode> specifies mode of writing to file (string)(default = overwrite); 
                append: append to file
                overwrite: overwrite file
            <delimit> specifies if, after write operation, 2 lines should be added
            to separate sections (string) (default = no separation)
                separate: add separation
                Other values: no separation (write directly on next line)
                
        Return: Null
        """
        
    # Set write mode to either append or overwrite (default overwrite)
        if mode == 'append' :
            self.write_mode = 'a';
        elif mode == 'overwrite' :
            self.write_mode = 'w';
        else :
            mode = 'overwrite';
            
        self.write_object = write_object;
        self.output_file = open(path, self.write_mode);
        
    # Check type for correct output method
        if (type(self.write_object) is list) == True :
        # Writes elements of a list on separate lines
            for i in range(0, len(self.write_object)) :
                self.output_file.write(str(self.write_object[i]) + '\n');
        elif (type(self.write_object) is str) == True :
        # Writes string as is
            self.output_file.write(self.write_object + '\n');
        elif (type(self.write_object) is int) == True :
        # Converts integar to string and write    
            self.output_file.write(str(self.write_object) + '\n');
        
        # Delimit with 2 new lines
        if delimit == 'separate' :
            self.output_file.write('\n'); 
            self.output_file.write('\n');
        
        self.output_file.close();