# zidryx
cryptography examples with python

## Diffie Hellman Key Exchange

Diffie-Hellman is a key agreement algorithm used by two parties to agree on a shared secret while communication over an insecure channel without requiring encryption. Even if an eavesdropper listens in, the shared secret can not be determined from the messages that are exchanged. There are many different variants and implementations of this algorithm since it was developed in 1976.

At first, the two parties agree on a shared set of parameters: a multiplicative group of integers modulo p, where p is a prime, usually a <a href="https://en.wikipedia.org/wiki/Safe_prime">safe prime</a>, and g a primitive root modulo p. Then both partners choose a secret. The first partner choses the secret a and computes g^a mod p, the other partner chooses b and computes g^b mod p. The result of this is shared with the partner over the channel. Then, the partners can each use the shared secret and raise it to the power of their own secret key modulo p, resulting in the values g^a^b and g^b^a, respectively, which are equivalent. 

![DH](https://github.com/LauraWartschinski/zidryx/blob/master/img/DiffieHellman.svg)

A common way to explain the process is to use the analogy of mixing colors. The common parameter g is the common paint (yellow) that both parties share. Red and blue are the secrets of both parties. Alice mixes yellow with red and sends orange to Bob, while Bob mixes yellow with blue and sends green to Alice. An eavesdropper can see the orange and green color, but is not able to 'de-mix' it and extract the original secret colors. By mixing orange with blue, Bob arrives and the final mixture, as does Alice with green and red, which is the common secret.

In the analogy, the mixing of colors is a simple, but irreversible process. In reality, computing g^a mod p is modular exponentiation, and can be done efficiently. However, the opposite operation is finding a secret key a, given only g, p and g^a mod p, which is the discrete logarithm problem. 

To make the protocol secure, the parameters have to be chosen properly. 