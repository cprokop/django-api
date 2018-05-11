class WarehouseRouter(object):
    """
    A router to control all database operations on models in
    the Warehouse application
    """
 
    def db_for_read(self, model, **hints):
        """
        Point all operations on Warehouse models to 'DB2'
        """
        if model._meta.app_label == 'Warehouse':
            return 'DB2'
        return None
 
    def db_for_write(self, model, **hints):
        """
        Point all operations on Warehouse models to 'other'
        """
        if model._meta.app_label == 'Warehouse':
            return 'DB2'
        return None
 
    def allow_syncdb(self, db, model):
        """
        Make sure the 'Warehouse' app only appears on the 'other' db
        """
        if db == 'DB2':
            return model._meta.app_label == 'Warehouse'
        elif model._meta.app_label == 'Warehouse':
            return False
        return None
