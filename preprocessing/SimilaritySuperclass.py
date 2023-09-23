from abc import ABC, abstractmethod
import csv


class SimilaritySuperclass(ABC):
    @abstractmethod
    def __similarityUserAToUserB__(self, user_A:tuple[str,...], user_B:tuple[str,...]) -> float:   
        """Function to implement, should provide a similarity value, 0 for no similarity and 1 for identical, direction is allowed to matter
        
        Args:
            userA (tuple[str,...]): the tuple of strings that define the user A
            userB (tuple[str,...]): the tuple of strings that define the user B
        
        Returns:
            float: the similarity of A to B, 0 for no similarity and 1 for identical
        """        
        pass
    
    @staticmethod
    @abstractmethod
    def __userDirectionMatters__() -> bool:
        """Whether it matters if for method __similarityUserAToUserB__ the input is (A,B)  or (B,A)
        
        Returns:
            bool: there exists A, B in the universe: __similarityUserAToUserB__(A,B) =! __similarityUserAToUserB__(B,A)
        """        
        pass
    
    def __init__(self, file: str, values_per_user: int, index_user_ids: int, *index_to_ignore: int) -> None:
        """Constructor for a similarity matrix class
        Args:
            file (str): the path to the file to draw the users from
            values_per_user (int): the number of values for each user
            index_user_ids (int): the index where the user ids are stored, user ids should be integers
            *index_to_ignore (int): each index to ignore, may include index_user_ids
        """        
        super().__init__()
        self.values_per_user: int = values_per_user
        self.index_to_ignore: int = index_to_ignore
        self.index_user_ids: tuple[int,...] = index_user_ids
        rows = []
        with open(file,'r') as f: reader:csv._reader = csv.reader(f, delimiter='\t')
        first_line = False
        for row in reader:
            if first_line:
                rows.append(row)
                print(row)
            else:
                first_line = True
        self.similarity_matrix: tuple[list[float]] = ([None]*len(rows),)*len(rows)
        self.user_ids_dictionary: dict[int, int]
        for i in range(len(rows)):
            self.user_ids_dictionary[rows[i][index_user_ids]] = i
            self.similarity_matrix[i][i] = 1.0
            for j in range(i):
                self.similarity_matrix[i][j] = self.__similarityUserAToUserB__(user_A=rows[i], user_B=rows[j])
                if self.__userDirectionMatters__():
                    self.similarity_matrix[j][i] = self.__similarityUserAToUserB__(user_A=rows[j], user_B=rows[i])
        
                
    
    def getSimilarityUserAToUserB(self, user_id_a: int, user_id_b: int):
        if not self.__userDirectionMatters__():
            a = user_id_a
            b = user_id_b
            user_id_a = max(a,b)
            user_id_b = min(a,b)
        return self.similarity_matrix[super.user_ids_dictionary[user_id_a]][super.user_ids_dictionary[user_id_b]]

class SimpleSimilarity(SimilaritySuperclass):
    def __init__(self, file: str, values_per_user: int, index_user_ids: int, *index_to_ignore: int) -> None:
        super().__init__(file, values_per_user, index_user_ids, *index_to_ignore)
        number_of_values_to_ignore = len(index_to_ignore)
        if not index_user_ids in index_to_ignore:
            number_of_values_to_ignore += 1
        self.factor: float = values_per_user - number_of_values_to_ignore
    
    def __similarityUserAToUserB__(self, user_A:tuple[str,...], user_B:tuple[str,...]) -> float:
        similarity_count: int = 0
        for i in range(super.values_per_user):
            if not (i in super.index_to_ignore or i is super.index_user_ids) and user_A[i] == user_B[i] and not user_A[i] == "":
                similarityCount += 1
        return similarity_count/self.factor
            
    def __userDirectionMatters__() -> bool:
        return False

SimpleSimilarity(file="dataset\users.tsv",values_per_user=15,index_user_ids=0,index_to_ignore=1,index_to_ignore=2)