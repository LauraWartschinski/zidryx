# zidryx
cryptography examples with python

## Diffie Hellman Key Exchange

This is a python implementation of a Diffie Hellman Key Exchange with simple sockets. Start two instances of the program which can reach each other over a network (or run them both locally) and use them to establish a shared symmetric key.

...or don't ;) This is just a very basic implementation that was created to explore the concept, understand it better, and to have some fun. But you should ***never just implement your own cryptography*** if you intend to use it for security-relevant purposes. Stick to the official libraries if you actually want to secure your communication. 

Now that this is out of the way...

### Background and Explanation

Diffie-Hellman is a key agreement algorithm used by two parties to agree on a shared secret while communication over an insecure channel without requiring encryption. Even if an eavesdropper listens in, the shared secret can not be determined from the messages that are exchanged. There are many different variants and implementations of this algorithm since it was developed in 1976.

At first, the two parties agree on a shared set of parameters: a multiplicative group of integers modulo p, where p is a prime, usually a <a href="https://en.wikipedia.org/wiki/Safe_prime">safe prime</a>, and g a primitive root modulo p. Then both partners choose a secret. The first partner choses the secret a and computes g^a mod p, the other partner chooses b and computes g^b mod p. The result of this is shared with the partner over the channel. Then, the partners can each use the shared secret and raise it to the power of their own secret key modulo p, resulting in the values g^a^b and g^b^a, respectively, which are equivalent. 

![DH](https://github.com/LauraWartschinski/zidryx/blob/master/img/DiffieHellman.svg)

A common way to explain the process is to use the analogy of mixing colors. The common parameter g is the common paint (yellow) that both parties share. Red and blue are the secrets of both parties. Alice mixes yellow with red and sends orange to Bob, while Bob mixes yellow with blue and sends green to Alice. An eavesdropper can see the orange and green color, but is not able to 'de-mix' it and extract the original secret colors. By mixing orange with blue, Bob arrives and the final mixture, as does Alice with green and red, which is the common secret.

In the analogy, the mixing of colors is a simple, but irreversible process. In reality, computing g^a mod p is modular exponentiation, and can be done efficiently. However, the opposite operation is finding a secret key a, given only g, p and g^a mod p, which is the discrete logarithm problem. 

### Choosing parameters

To make the protocol secure, the parameters have to be chosen properly. The order of the group of integers must be large, otherwise there are <a href="https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange">ways to attack the algorithm</a>. By chosing a safe prime for p, p = 2q+1 with q being a prime number, the order of the group is only divisible by 2 and q. In such a case, q is also called a <a href="https://en.wikipedia.org/wiki/Sophie_Germain_prime">Germaine Prime</a>. This makes it way easier to find a generator g, since g is a generator iff for every prime factor q of p-1, g ^ (p-1)/q is not congruent to 1 modulo p. This is way easier to test if q and 1 are the only prime factors of p-1. For Diffie Hellman, 2 is usually used as a generator, even if it doesn't truly generate the whole group, but only a subgroup (all the possible values g^k mod p can take), as this prevents leaking some bits of the private key if the generator has small factors. 

The secret keys should have at least around 180 bits of entropy, or more, and should not have the value 0 or p-1. Following what is outlined in <a href="https://datatracker.ietf.org/doc/rfc3526/?include_text=1">RFC 3526</a>, the secret key, which is the exponent for the operations in the Diffie Hellman algorithm, should consist of twice the amount of bits than the strength of the group. 

Luckily, there are already some recommended values. This implementation uses the values specified in <a href="https://datatracker.ietf.org/doc/rfc3526/?include_text=1">RFC 3526</a> in the  Modular Exponential Group Nr. 14, a 1028 bit group with a prime which has the hexadecimal value:

```
      FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
      29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
      EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
      E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
      EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
      C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
      83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
      670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
      E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
      DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
      15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
```
      
The group is to be used with the generator 2 and estimated to have a strength of 110 - 160 bit. 
      
One more remark: The Diffie Hellman Key Exchange does not authenticate users. A man in the middle attack can be used to establish to seperate keys, one between the attacker and Alice, and one between the attacker and Bob. This is of course not a concern if the attacker can only read, but not modify messages. However, to prevent against modified messages, some other form of authentication must be used. 

### The implementation

This implementation lets the user pick either the role of Alice or Bob. The users need a working network connection between them. The protocol itself is basically symmetric, but for simplicity's sake, only one side gets to propose the parameters for the algorithm. Both users start the program and pick different roles. Alice is then asked to enter the partner's IP address, and the exchange between the two partners is initiated after Alice sends "DH" to Bob and he replies with the same.
 
Alices has to specify the length of the private keys as well as the values for the modulus p and the generator g, while it is suggested to her to use the default value. Some checks are performed on the parameters, before they are sent to Bob, who will also perform some checks and reject the whole exchange if the parameters are not chosen well. Next, for both partners, a random private key of the desired length in bits is created and taken as exponent to calculate the shared secret g^a mod p.

Alice sends her shared secret to Bob, who receives it and replies with his shared secret. Now, both sides can compute the final common secret and display it to the user. 

![screenshot](https://github.com/LauraWartschinski/zidryx/blob/master/img/dh.png)
