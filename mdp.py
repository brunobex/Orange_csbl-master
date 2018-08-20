import random
import Orange

from Orange.data import Domain, Table

print (( "Number of attributes: %s") % (len(in_data.domain)))
print (( "Number of instances: %s") % (len(in_data)))

domain = Domain([attr for attr in in_data.domain.attributes if attr.is_continuous or len(attr.values) <- 5], in_data.domain.class_vars)

out_data = Table(domain, in_data)



