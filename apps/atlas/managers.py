from django.db.models import Manager

class SpodManager(Manager):
    """
    Spod manager
    
    """
    def get_query_set(self):
        """
        Get active objects only everytime.
        
        """
        return super(SpodManager,  self).get_query_set()
    
    def get_by_coordinates(self, coordinates):
        try:
            return self.get(coordinates=coordinates)
        except:
            return False
    
    def public(self):
        return self.get_query_set().filter(status__gte=2)
        
    def search(self, search_terms):
        from libs.search import normalize
        terms = normalize(search_terms)
        q_objects = []
        
        for term in terms:
            q_objects.append(models.Q(title__icontains=term))
            q_objects.append(models.Q(spotline__icontains=term))
            # q_objects.append(models.Q(tags__icontains=term))
        
        # Start with a bare QuerySet
        qs = self.get_query_set()
        
        # Use operator's or_ to string together all of your Q objects.
        return qs.filter(reduce(operator.or_, q_objects))

class FavoriteManager(Manager):
    """
    Node manager
    
    """
    def get_query_set(self):
        """
        Get active objects only everytime.
        
        """
        return super(FavoriteManager,  self).get_query_set().filter(spod__status=2)
        
