from np_neural_network import np_network
import numpy as np
import random

class np_recurrent_network(np_network) :
    
    def __init__(self, iS, hS, oS) :
        # todo: (maybe) support multiple hidden layers
        np_network.__init__(self, iS, hS, oS, 1)
        self.r_weights = np.array(0)
        self.reset_last()

    def prop_network(self, set_last_state = True) :
        res = np.dot(self.input, self.i_weights)
        r_res = self.calced_last_state
        res += r_res
        res = self.activate(res)
        # save the recurrent state for next propogation
        if set_last_state :
            self.last_state = res
        # in case we need it later but don't want it to affect future calculations (yet)
        self.tmp_last_state = res
        # todo: (maybe) support multiple hidden layers
        res = np.dot(res, self.o_weights)
        self.output = self.activate(res)

    def prop_input(self, vals, set_last_state = True) :
        np_network.set_input(self, vals)
        self.prop_network(set_last_state)
        return self.get_output()

    def set_last_state(self, vals) :
        self.last_state = vals
        if self.r_weights.any() :
            self.calced_last_state = np.dot(self.last_state, self.r_weights)


    def randomize_weights(self, rand = np.random) :
        np_network.randomize_weights(self, rand)
        self.r_weights = self.scale_random(rand.rand(self.h_size, self.h_size))
        # do this to make sure calced_last_state is set
        self.set_last_state(self.last_state)


    def export_weights(self) :
        res = np_network.export_weights(self)
        for r in self.r_weights :
            res.extend(r.tolist())
        return res

    def import_weights(self, vals) :
        np_network.import_weights(self, vals)
        vals = vals[np_network.get_network_size(self):]
        self.r_weights = np.array([vals[x:x+self.h_size] for x in range(0, self.h_size * self.h_size, self.h_size)])
        self.reset_last()

    def reset_last(self):
        self.set_last_state(np.zeros(self.h_size))
    
    def get_network_size(self) :
        return np_network.get_network_size(self) + self.h_size * self.h_size


if __name__ == "__main__" :
        rec_net = np_recurrent_network(3, 4, 2)
        ner_net = np_network(3, 4, 2)
        rec_net.randomize_weights()
        ner_net.import_weights(rec_net.export_weights()[:ner_net.get_network_size()])
        # print rec_net.export_weights()
        stepCount = 3
        inps = [tuple(random.random() * 2 - 1 for x in range(0, rec_net.i_size)) for x in range(0, stepCount)]
        # repeat each input once so we can see the recurrent information affect it
        for x in range(0, stepCount * 2) :
            rec_net.prop_input(inps[int(x / 2)])
            ner_net.prop_input(inps[int(x / 2)])
            print rec_net.get_output(), '\t\t', ner_net.get_output(), '\n'
        
        print rec_net.last_state


