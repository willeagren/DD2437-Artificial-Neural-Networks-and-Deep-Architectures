from util import *
from rbm import RestrictedBoltzmannMachine 
from dbn import DeepBeliefNet

if __name__ == "__main__":

    image_size = [28,28]
    train_imgs,train_lbls,test_imgs,test_lbls = read_mnist(dim=image_size, n_train=60000, n_test=10000)

    ''' restricted boltzmann machine '''
    
    #print ("\nStarting a Restricted Boltzmann Machine..")

    rbm = RestrictedBoltzmannMachine(ndim_visible=image_size[0]*image_size[1],
                                     ndim_hidden=500,
                                     is_bottom=True,
                                     image_size=image_size,
                                     is_top=False,
                                     n_labels=10,
                                     batch_size=10
    )
    
    loss_list = rbm.cd1(visible_trainset=train_imgs, n_iterations=10)

    #plt.plot([x for x in range(len(loss_list))], loss_list, label="500 hidden units")
    #plt.xlabel("Epochs")
    #plt.ylabel("Reconstruction MSE")
    #plt.legend()
    #plt.grid()
    #plt.show()
    
    ''' deep- belief net '''

    print ("\nStarting a Deep Belief Net..")
    
    dbn = DeepBeliefNet(sizes={"vis":image_size[0]*image_size[1], "hid":500, "pen":500, "top":2000, "lbl":10},
                        image_size=image_size,
                        n_labels=10,
                        batch_size=20
    )
    
    ''' greedy layer-wise training '''

    recon_list = dbn.train_greedylayerwise(vis_trainset=train_imgs, lbl_trainset=train_lbls, n_iterations=10)

    layer_label = {
        0: "vis--hid",
        1: "hid--pen",
        2: "pen+lbl--top"
    }

    for i in range(len(recon_list)):
        it = [x for x in range(1, len(recon_list[i]) + 1)]
        plt.plot(it, recon_list[i], label=layer_label[i])
    plt.grid()
    plt.xlabel("Epoch")
    plt.ylabel("Reconstruction MSE")
    plt.legend()
    plt.show()

    # RECOGNIZE WORKS GREAT!
    print(f" ### -- DBN recognize with training data -- ###")
    dbn.recognize(train_imgs, train_lbls)
    print(f" ### -- DBN recognize with test data -- ###")
    dbn.recognize(test_imgs, test_lbls)

    for digit in range(10):
        digit_1hot = np.zeros(shape=(1,10))
        digit_1hot[0, digit] = 1
        print(digit_1hot)
        dbn.generate(digit_1hot, "rbms", digit)
"""
    ''' fine-tune wake-sleep training '''

    dbn.train_wakesleep_finetune(vis_trainset=train_imgs, lbl_trainset=train_lbls, n_iterations=10000)

    dbn.recognize(train_imgs, train_lbls)
    
    dbn.recognize(test_imgs, test_lbls)
    
    for digit in range(10):
        digit_1hot = np.zeros(shape=(1,10))
        digit_1hot[0,digit] = 1
        dbn.generate(digit_1hot, name="dbn")
"""