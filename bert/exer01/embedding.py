import tensorflow
from tensorflow import SummaryWriter
writer = SummaryWriter()
# 100个词汇表示成50维的向量
embedded = torch.randn(100, 50)
# 导入100个中文词汇
meta = list(map(lambda x: x.strip(), fileinput.fileInput("./vocab100.csv")))
writer.add_embedding(embedded, metadata=meta)
writer.close()
