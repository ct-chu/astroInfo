import matplotlib.pyplot as plt

fig,ax = plt.subplots(figsize=(4,2))
ax.set_aspect('equal')
ax.set_xlim((-1,5))
ax.set_ylim((-2,2))
lw = 28
ax.plot([0,4],[0,0],c='r',lw=lw)
ax.plot([1,1],[-1,1],c='r',lw=lw)
ax.plot([3,3],[-1,1],c='r',lw=lw)
plt.show()
