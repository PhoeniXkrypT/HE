import numpy

# defining the big O constant and lambda value
bigOconstant = 2
lambda_value = 8

def main():
	sk = secret_key(lambda_value)	# function call to generate secret key
	print "Secret Key\n", int(sk)
	pk = public_key(sk)		# function call to generate public key list
	print "Public Key Values\n", pk
	random_subset = generate_random_subset(tau(lambda_value))
	m = numpy.random.randint(0,2)
	print " Message = ", m
	c = encrypt(pk, m, random_subset)
	print " Cipher = ", c

# Function to calculate eta value from the security parameter lambda
def eta(lambda_value):			# eta is bit length of secret key 
	return (bigOconstant * lambda_value * lambda_value)
# Function to calculate gamma value from the security parameter lambda
def gamma(lambda_value):
	return (bigOconstant * lambda_value**5)
# Function to calculate tau value from the security parameter lambda
def tau(lambda_value):			# tau is number of integers in public key
	return (gamma(lambda_value) + lambda_value)
# Function to calculate rho' value from security parameter lambda
def rho_dash(lambda_value):
	return (2*lambda_value)
	
# Function to calculate the secret key which is an odd eta-bit integer
def secret_key(lambda_value):
	eta_value = eta(lambda_value)
	number_count = eta_value / 32
	base = 2**32
	# generate the secret key by taking four numbers and concatinating them using a base
	# number = x3*base**3 + x2*base**2 + x1*base + x0
	while True :
		rand_numbers = [int(numpy.random.uniform(0,2**32)) for x in xrange(number_count -1)]
		if (int(rand_numbers[0]) & 1) :
			break
	concatenated_number = rand_numbers[0] + rand_numbers[1] * base + rand_numbers[2] * base**2
	msb_number = int(numpy.random.uniform(2**31,2**32))
	secret_key = concatenated_number + (msb_number * base**3)
	return secret_key
	
# Function to find the different values of public key
def distribution(secret_key):
	#q_bound = 2**gamma(lambda_value) / secret_key
	q = int(numpy.random.uniform(0,2**256))		
	r = int(numpy.random.uniform(-2**lambda_value, 2**lambda_value))
	x = secret_key * q + r
	return x
	
# Function to calculate the public key list
def public_key(secret_key):
	while True:
		pubkey = [distribution(secret_key) for i in range(tau(lambda_value))]
		pubkey_max = max(pubkey)	# get largest value from list	
		pubkey_mod_sk = pubkey_max % secret_key
		# loop till largest value is odd and the value modulus secret key is even
		if (pubkey_max & 1) and (pubkey_mod_sk % 2 == 0):
			break
	return pubkey

# Function to generate a random subset S from {1, 2, 3, .... tau}
def generate_random_subset(_tau):
	set_size = numpy.random.randint(1, _tau)
	S = set()
	while len(S) < set_size:
		x = numpy.random.randint(1, _tau)
		S.add(x)
	return S

# Function to encrypt a bit m from {0,1}	
def encrypt(public_key, m, S):
	# c = (m+2r+2*xi's) mod x0
	# Sorting in descending order
	pub_key_sorted = sorted(public_key, reverse=True)
	rho_dash_value = rho_dash(lambda_value)
	r = int(numpy.random.randint(-2**rho_dash_value, 2**rho_dash_value))
	sum_x = 0
	# the summation of xi's for i belongs to S i.e subset of {1,2,3 ... tau}
	for i in S:
		sum_x += public_key[i]
	cipher = (m + 2*r + 2*sum_x ) % pub_key_sorted[0]
	return cipher

if __name__ == "__main__":
    main()