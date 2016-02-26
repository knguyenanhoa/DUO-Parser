class AnalysisMethod :
    """
    Analysis methods for DUO data.
    """
    
    def __init__(self) :
        """
        Initializes necessary variables for this class
        """
    
    def TwoMatrixOperation(self, start_object_1, start_object_2, formula):
        """
        Macro for 2D matrix manipulation
        
        Arguments: 
            <start_object_1>, <start_object_2> specifies matrices to be transformed 
            (list), (list)
            <formula> specifies method of matrix transformation (string)
                dim: return matrix dimensions (set start_object_2 to 0);
                add: add 2 matrices
                sub: subtract 2 matrices
                mult: multiply 2 matrices element by element
                div: divide 2 matrices element by element
            
        Return: List
        """ 
        # Declare variables
        i_1 = 0;
        i_2 = len(start_object_1);
        j_1 = 0;
        j_2 = len(start_object_1[0]);
        x_dim = 0;
        y_dim = 0;
        
        # Initialize result matrix
        result_object = [[0 for i in range(i_1, i_2)] for j in range(j_1, j_2)];    
        
        # Matrix x by y dimensions stored in result array at pos
        # x = [0][0] and y = [0][1]
        if (formula == "dim") :
            x_dim = len(start_object_1); 
            y_dim = len(start_object_1[0]);
        
        result_object[0][0] = x_dim;
        result_object[0][1] = y_dim;
        
        # Matrix addition
        if (formula == "add") :
            for i in range(i_1, i_2) :
                for j in range(j_1, j_2) :
                    result_object[i][j] = (start_object_1[i][j] + 
                                              start_object_2[i][j]);
        
        # Matrix subtraction
        if (formula == "sub") :
            for i in range(i_1, i_2) :
                for j in range(j_1, j_2) :
                    result_object[i][j] = (start_object_1[i][j] - 
                                            start_object_2[i][j]);
        
        # Matrix multiplication element wise
        if (formula == "mult") :
            for i in range(i_1, i_2) :
                for j in range(j_1, j_2) :
                    result_object[i][j] = (start_object_1[i][j] * 
                                            start_object_2[i][j]);
        # Matrix division element wise
        if (formula == "div") :
            for i in range(i_1, i_2) :
                for j in range(j_1, j_2) :
                    if (start_object_2[i][j]) == 0 :
                        result_object[i][j] = 0;
                    elif (start_object_2[i][j] != 0) :
                        result_object[i][j] = (start_object_1[i][j] / 
                                               start_object_2[i][j]);
                    
        return(result_object);