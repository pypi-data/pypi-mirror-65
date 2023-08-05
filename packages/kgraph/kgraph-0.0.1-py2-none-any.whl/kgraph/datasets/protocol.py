import numpy as np
import multiprocessing as mp


# Add the reverse data to original data.
def add_reverse(data, num_relations, concate=True):
    if concate:
        src_, rel, dst_ = data.transpose(1, 0)
        src = np.concatenate((src_, dst_), 0)
        rel = np.concatenate((rel, rel + num_relations), 0)
        dst = np.concatenate((dst_, src_), 0)
        
        data = np.stack((src, rel, dst)).transpose(1, 0)
    else:
        data[:, 1] += num_relations
    return data

# Get the graph triplets
def get_train_triplets_set(train_data):
    return set([(x[0], x[1], x[2]) for x in train_data])


def __negative_sample_with_label(pos_samples, global_triplets,
                                 total_entities, size, negative_rate):
    num_to_generate = size * negative_rate
    neg_samples = np.tile(pos_samples, (negative_rate, 1))
    labels = np.ones(size * (negative_rate + 1), dtype=np.float32) * (-1.)
    labels[: size] = 1
    
    values = np.random.randint(total_entities, size=num_to_generate)
    choices = np.random.uniform(size=num_to_generate)
    subj = choices > 0.5
    obj = choices <= 0.5
    neg_samples[subj, 0] = values[subj]
    neg_samples[obj, 2] = values[obj]
    
    for i, p in enumerate(choices):
        while True:
            triplet = (neg_samples[i, 0], neg_samples[i, 1], neg_samples[i, 2])
            if triplet not in global_triplets:
                break
            if p > 0.5:
                neg_samples[i, 0] = np.random.choice(total_entities)
            else:
                neg_samples[i, 2] = np.random.choice(total_entities)
                
    return np.concatenate((pos_samples, neg_samples)), labels

def generate_batch_with_neg_and_labels(train_data, global_triplets, total_entities,
                   batch_size=512, negative_rate=5):
    size = len(train_data)
    num_batch = size // batch_size + 1
    train_data = np.random.permutation(train_data)
    
    for i in range(num_batch):
        yield __negative_sample_with_label(train_data[i * batch_size : (i + 1) * batch_size, :],
                                global_triplets, total_entities, size, negative_rate)

