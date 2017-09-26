#!/use/bin/python
'''
File name: pim.py
File desc: Parallel iterative matching using randomness
Date: 	   Sep 26, 2017
'''
import sys
import random


class SwitchSchedule():
	"""
	"""
	def __init__(self, traffic):
		
		self.raw_traffic = traffic
		self.n = 0	# n X n switch
		self.input_ports = {}
		self.output_ports = {}
		self.parse(traffic)
		self.rounds = {}

	def print_iteration_requests(self, rounds, iter, requests):
		"""
		"""
		print "round:", rounds
		print "iteration:", iter
		print "Request Phase:"
		print "o/p", "\t", "requests"
		for i in range(self.n):
			if i > len(requests):
				print i+1, "\t", "-"
				continue
			print i+1, "\t", requests[i]
		print

	def print_iteration_granted(self, granted):
		"""
		"""
		print "Granted Phase:"
		print "o/p", "\t", "granted i/p"
		for i in range(self.n):
			if i > len(granted):
				print i+1, "\t", "-"
				continue
			print i+1, "\t", granted[i][1]
		print

	def print_iteration_grants(self, grants):
		"""
		"""
		print "i/p", "\t", "grants got"
		for i in range(self.n):
			if i > len(grants):
				print i+1, "\t", "-"
				continue
			if type(grants[i]) is tuple:
				print i+1, "\t", []
				continue
			print i+1, "\t", grants[i]
		print

	def print_iteration_accepted(self, accepted):
		"""
		"""
		print "Accepted Phase:"
		print "i/p", "\t", "accepted o/p"
		for i in range(self.n):
			if i > len(accepted):
				print i+1, "\t", "-"
				continue
			print i+1, "\t", accepted[i][1]
		print

	def printtotal(self):
		"""
		"""
		print "Round\tIterations"
		for i in range(1, len(self.rounds)+1):
			print i, "\t", self.rounds[i]
		print

	def parse(self, traffic):
		"""
		"""
		traffic = traffic.split("\n")
		self.n = int(traffic[0])
		print "Switch Type: ", self.n, "X", self.n
		for i in range(1, self.n+1):
			#print traffic[i].split()
			self.input_ports[i] = {
				'R': [0] * (self.n + 1),	# Requests for output ports
				'Gd': [0] * (self.n + 1),	# Grant Received from output
				'A' : -1					# grant which it Accepts
			}
			for each in traffic[i].split():
				try:
					self.input_ports[i]['R'][int(each)] = 1
				except:
					break

		for i in range(1, self.n+1):
			self.output_ports[i] = {
				'Rd': [0] * (self.n + 1),	# Request Received from input
				'G': -1,					# Grant sent to input
				'Ad' : 0					# grant which got Accepted
			}

	def run(self):
		"""
		"""
		rounds = 0
		while True:
			rounds += 1
			iterations = 0
			while True:
				iterations += 1
				all_requests = []
				granted = []
				accepted = []
				for k in range(1, len(self.output_ports) + 1):
					requests = []
					for i in range(1, len(self.input_ports) + 1):
						# Step 1. Acknowledge the requests from each input port
						# 		  if there is one
						# "if there is a request for kth output port at ith
						# input port"
						if self.input_ports[i]['A'] == -1:
							# only if it hasn't accepted an output port already
							# in this round
							self.output_ports[k]['Rd'][i] = \
								self.input_ports[i]['R'][k]
							if self.output_ports[k]['Rd'][i] is 1:
								requests.append(i)
					
					# print requests
					all_requests.append(requests)
					# Step 2. Grant a request randomly for kth output port
					try: 
						g = random.choice(requests)
					except IndexError:
						granted.append((k, []))
						continue
					granted.append((k, g))
					self.output_ports[k]['G'] = g
					self.input_ports[g]['Gd'][k] = 1

				self.print_iteration_requests(rounds, iterations, all_requests)
				self.print_iteration_granted(granted)
				
				all_grants = []
				for i in range(1, len(self.input_ports) + 1):
					if self.input_ports[i]['A'] == -1:
						# only if it hasn't accepted an output port already in
						# this round
						grants = [q for q, x in enumerate(
							self.input_ports[i]['Gd']) if x is 1]
						# Step 3. Accept a grant randomly out of all received
						#print grants
						all_grants.append(grants)
						try:
							a = random.choice(grants)
						except IndexError:
							accepted.append((i, []))
							continue
						#print "rhjk", i, a
						accepted.append((i, a))
						self.input_ports[i]['A'] = a
						self.output_ports[a]['Ad'] = 1
						self.input_ports[i]['R'][a] = 0
					else:
						all_grants.append((i, []))
						accepted.append((i, []))

				self.print_iteration_grants(all_grants)
				self.print_iteration_accepted(accepted)
				
				remaining_ips = 0
				for i in range(1, len(self.input_ports) + 1):
					if self.input_ports[i]['A'] == -1 and \
						1 in self.input_ports[i]['R']:
						remaining_ips += 1

				if remaining_ips == 0:
					break

			remaining_reqs = 0
			for i in range(1, self.n+1):
				if 1 in self.input_ports[i]['R']:
					self.input_ports[i]['Gd'] = [0] * (self.n + 1)
					self.input_ports[i]['A'] = -1
					remaining_reqs += 1

			self.rounds[rounds] = iterations
			if remaining_reqs == 0:
				break

			for i in range(1, self.n+1):
				self.output_ports[i] = {
					'Rd': [0] * (self.n + 1),
					'G': -1,
					'Ad' : 0
				}

		self.printtotal()

if __name__ == '__main__':
	print "Usage: python pim.py < input_traffic_file"
	result = sys.stdin.read()
	s = SwitchSchedule(result)
	s.run()
