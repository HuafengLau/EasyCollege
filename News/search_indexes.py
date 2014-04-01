#coding:utf-8

import datetime
from haystack import indexes
from News.models import News, NewsPart

class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True,template_name='News/news_text.txt')
    user = indexes.CharField(model_attr='user')
    time = indexes.DateTimeField(model_attr='time')
    type = indexes.CharField(model_attr='type')
    newspart = indexes.CharField(model_attr='newspart')

    def get_model(self):
        return News
        
    def prepare_user(self, obj):
        return u'%s' % obj.user.nic_name
        
    def prepare_newspart(self, obj):
        return u'%s / %s' % (obj.newspart.part, obj.newspart.realPart)

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
        
class NewspartIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True,template_name='News/newspart_text.txt')

    def get_model(self):
        return NewsPart

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
        

