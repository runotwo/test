import pandas as pd
import seaborn as sns

df = pd.read_json('rest/rest.json')

df2 = pd.read_json('rest/urest.json')
df = pd.concat([df, df2], ignore_index=True, sort=True)

df2 = pd.read_json('message_pack/message_pack.json')
df = pd.concat([df, df2], ignore_index=True, sort=True)

df2 = pd.read_json('helloworld/grpc.json')
df = pd.concat([df, df2], ignore_index=True, sort=True)

df2 = pd.read_json('protobuf/protobuf.json')
df = pd.concat([df, df2], ignore_index=True, sort=True)

df2 = pd.read_json('rabbitmq/mq.json')
df = pd.concat([df, df2], ignore_index=True, sort=True)

qq = sns.boxplot(x='method', y='rps', hue='size', data=df)
fig = qq.figure
fig.savefig('violinplot.png')
qq = sns.catplot(x='method', y='rps', hue='size', data=df, kind="bar", palette="muted")
qq.savefig('catplot.png')