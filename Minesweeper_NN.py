import numpy as np
import torch as tr
from torch.nn import Sequential, Conv2d, Linear, Flatten, LeakyReLU, Tanh, ReLU

def MSNet1(r_grid,c_grid):
    ms_model = Sequential(
        Flatten(),
        Linear(5*(r_grid*c_grid),2),
        ReLU(),
        Linear(2,1)
    )
    return ms_model

# def MSNet2(r_grid,c_grid):
#     ms_model = Sequential(
#         Conv2d(5,2,kernel_size=(r_grid,c_grid))
#     )
#     return ms_model


def calculate_loss(net, x, y_targ):
    y = net(x)
    e = tr.sum((y-y_targ)**2)
    return (y,e)

def optimization_step(optimizer, net, x, y_targ):
    optimizer.zero_grad()
    y,e = calculate_loss(net,x,y_targ)
    e.backward()
    optimizer.step()
    return (y,e)

if __name__ == "__main__":

    r, c = map(int, input('Enter the Grid Size : (row,column)').split(','))
    net = MSNet1(r_grid=r,c_grid=c)
    print(net)

    import pickle as pk
    with open("data-%dX%d.pkl" %(r,c),"rb") as f: (x, y_targ) = pk.load(f)

    # Optimization loop
    optimizer = tr.optim.Adam(net.parameters())
    train_loss, test_loss = [], []
    shuffle = np.random.permutation(range(len(x)))
    split = 10
    train, test = shuffle[:-split], shuffle[-split:]
    for epoch in range(500):
        y_train, e_train = optimization_step(optimizer, net, x[train], y_targ[train])
        y_test, e_test = calculate_loss(net, x[test], y_targ[test])
        if epoch % 10 == 0: print("%d: %f (%f)" % (epoch, e_train.item(), e_test.item()))
        train_loss.append(e_train.item() / (len(shuffle)-split))
        test_loss.append(e_test.item() / split)
    
    tr.save(net.state_dict(), "model-%dX%d.pth" % (r,c))
    
    import matplotlib.pyplot as pt
    pt.plot(train_loss,'b-')
    pt.plot(test_loss,'r-')
    pt.legend(["Train","Test"])
    pt.xlabel("Iteration")
    pt.ylabel("Average Loss")
    pt.show()
    
    pt.plot(y_train.detach().numpy(), y_targ[train].detach().numpy(),'bo')
    pt.plot(y_test.detach().numpy(), y_targ[test].detach().numpy(),'ro')
    pt.legend(["Train","Test"])
    pt.xlabel("Actual output")
    pt.ylabel("Target output")
    pt.show()
