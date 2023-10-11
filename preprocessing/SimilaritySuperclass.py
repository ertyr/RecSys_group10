from abc import ABC, abstractmethod
import pickle
import pandas as pd

from tools.Distance import distance, location_user


class SimilaritySuperclass(ABC):
    @abstractmethod
    def __similarityUserAToUserB__(self, user_A:pd.DataFrame, user_B:pd.DataFrame) -> float:   
        """Function to implement, should provide a similarity value, 0 for no similarity and 1 for identical, direction is allowed to matter
        
        Args:
            userA (tuple[str,...]): the tuple of strings that define the user A
            userB (tuple[str,...]): the tuple of strings that define the user B
        
        Returns:
            float: the similarity of A to B, 0 for no similarity and 1 for identical
        """        
        pass
    
    @abstractmethod
    def __userDirectionMatters__(self) -> bool:
        """Whether it matters if for method __similarityUserAToUserB__ the input is (A,B)  or (B,A)
        
        Returns:
            bool: there exists A, B in the universe: __similarityUserAToUserB__(A,B) =! __similarityUserAToUserB__(B,A)
        """        
        pass
    
    def __preProcessDataFrame(self, df: pd.DataFrame) -> pd.DataFrame:
        return df
    
    def __init__(self, df: pd.DataFrame, serialized_file_name: str = None) -> None:
        """Constructor for a similarity matrix class
        Args:
            file (str): the path to the file to draw the users from
            values_per_user (int): the number of values for each user
            index_user_ids (int): the index where the user ids are stored, user ids should be integers
            *index_to_ignore (int): each index to ignore, may include index_user_ids
        """        
        super().__init__()
        df = self.__preProcessDataFrame(df)
        self.user_to_user_similarity: dict[int, dict[int, float]] = {}
        indexes = df.index
        for k in range(len(indexes)):
            i = indexes[k]
            self.user_to_user_similarity[i] = {}
            self.user_to_user_similarity[i][i] = 1.0
            a = df.loc[[i]]
            for j in indexes[:k]:
                b = df.loc[[j]]
                self.user_to_user_similarity[i][j] = self.__similarityUserAToUserB__(user_A=a, user_B=b)
                if self.__userDirectionMatters__():
                    self.user_to_user_similarity[j][i] = self.__similarityUserAToUserB__(user_A=b, user_B=a)
                else:
                    self.user_to_user_similarity[j][i] = self.user_to_user_similarity[i][j]
            print(k,"/",len(indexes))
        if serialized_file_name == None:
            serialized_file_name = str(type(self).__name__)+'.pkl'
        with open(serialized_file_name, 'wb') as f:
            pickle.dump(self.user_to_user_similarity, f)
        
    def getSimilarityUserAToUserB(self, user_id_a: int, user_id_b: int):
        return self.user_to_user_similarity[user_id_a][user_id_b]
    
class DeserializedSimilarityClass(SimilaritySuperclass):
    def __init__(self, serialized_class_file: str, user_direction_matters) -> None:
        self.user_direction_matters = user_direction_matters
        with open(serialized_class_file, 'rb') as f:
            super().user_to_user_similarity = pickle.load(f)
    
    def __userDirectionMatters__(self) -> bool:
        return self.user_direction_matters

class SimilaritySuperclassTest(SimilaritySuperclass):
    def __init__(self, file: str, serialized_file_name: str = None) -> None:
        super().__init__(file, serialized_file_name)
    def __similarityUserAToUserB__(self, user_A:pd.DataFrame, user_B:pd.DataFrame) -> float:
        return 1.0
    def __userDirectionMatters__(self) -> bool:
        return False
    
class SimilaritySuperclassDistance(SimilaritySuperclass):
    def __init__(self, file: str, serialized_file_name: str = None) -> None:
        super().__init__(file, serialized_file_name)
    def __similarityUserAToUserB__(self, user_A:pd.DataFrame, user_B:pd.DataFrame) -> float:
        d = distance(location_a=location_user(user_A), location_b=location_user(user_B))
        max_distance = 40075
        return 1 - d / max_distance
    def __userDirectionMatters__(self) -> bool:
        return False

def demo1():
    df: pd.DataFrame = pd.read_table('dataset/users.tsv', index_col='UserID')
    max_demo_index = 100
    df = df.iloc[range(max_demo_index)]
    SimilaritySuperclassTest(df, "DEMO")

def demo2():
    df: pd.DataFrame = pd.read_table('dataset/users.tsv', index_col='UserID')
    max_demo_index = 10
    df = df.iloc[range(max_demo_index)]
    SimilaritySuperclassDistance(df, "DEMO")
