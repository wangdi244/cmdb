#!/usr/bin/env python    
#coding=utf-8

from app.models import ContainsList, ContainsList_Develop,ContainsList_Test
from haystack import indexes

class ContainsListIndex(indexes.SearchIndex, indexes.Indexable):  
    text = indexes.CharField(document=True, use_template=True)      
    
    def get_model(self):  
        return ContainsList
    
    def index_queryset(self,using=None): 
        """Used when the entire index for model is updated."""    
        return self.get_model().objects.all()

class ContainsList_DevelopIndex(indexes.SearchIndex, indexes.Indexable):  
    text = indexes.CharField(document=True, use_template=True)      
    
    def get_model(self):  
        return ContainsList_Develop
    
    def index_queryset(self,using=None): 
        """Used when the entire index for model is updated."""    
        return self.get_model().objects.all()

class ContainsList_TestIndex(indexes.SearchIndex, indexes.Indexable):  
    text = indexes.CharField(document=True, use_template=True)      
    
    def get_model(self):  
        return ContainsList_Test
    
    def index_queryset(self,using=None): 
        """Used when the entire index for model is updated."""    
        return self.get_model().objects.all()



