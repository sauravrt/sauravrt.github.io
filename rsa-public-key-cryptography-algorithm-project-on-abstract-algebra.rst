RSA : Public Key Cryptography Algorithm ( Project on Abstract Algebra )
#######################################################################
:date: 2011-12-26 20:31
:author: sauravtuladhar
:category: Programming, Python
:slug: rsa-public-key-cryptography-algorithm-project-on-abstract-algebra
:status: published

Abstract Algebra was one of the mathematics course I took for the Fall semester which has just ended. The complete course has two parts taught over two semesters. I took the first part and it mainly covered some basic Number Theory and largely Group Theory. As a part of the project I had to a class project and my choice was RSA : A Public Key Cryptography Algorithm. The strength of RSA is based on difficulty in factoring large integers, specially those formed as product of two integers.  The algorithm uses Number Theory concepts of modulo exponentiation, the Euler's function and the decryption is based on Euler's theorem. My objectives were to study the algorithm itself and do a simple implementation.

In public key cryptography, the key has a *public part* and a *private part*. The public part is made known to everybody where as the private part is kept secret by the receiver ( My PGP `public key <http://sauravtuladhar.info/pgp-public-key/>`__ ). Anyone who intends to send a message to the receiver encrypts the plaintext using the public key corresponding to the receiver. Once encrypted using the public key, the ciphertext can only be decrypted using the private key, which is safe with the receiver.

RSA is a public key cryptography algorithm jointly developed by R. Rivest, A. Shamir and L. Adleman and it was described in  a `paper <http://dl.acm.org/citation.cfm?id=359342>`__ in 1978. The name of the algorithm comprises of the first letters of the three authors surnames.  The algorithm was originally patented by M.I.T. but was released to public domain in September 2000. The algorithm has three steps (1) Key generation (2) Encryption (3) Decryption.

Key Generation

| The RSA key pair is generated as follows
| \* Generate a pair of prime numbers $latex *p$* and $latex q\ *$*
| \* Compute $latex *n = pq$$*
| \* Compute the Euler's function $latex \\phi(n) = (p - 1)(q - 1)$
| \* Find an integer $e$ such that $latex 1 < e < \\phi(n)$ and is coprime with $latex \\phi(n)$ i.e. $gcd(e,\phi(n)) = 1$.
| \* Find another integer $latex d$ such that $latex de \\equiv 1~\text{mod}(\phi(n))$. This is determined using extended Euclidean algorithm which gives $latex ed + k\phi(n) = 1$ where $k$ is some integer.
| The public key consists of the pair $latex (e, n)$ and the private key consists of the pair $latex (d, n)$.

Encryption and Decryption

RSA algorithm uses modulo exponentiation operation for both encryption and decryption. The plaintext is first converted to numeric codes before they are encrypted. For instance, the letters in the plaintext are represented as integers $latex x$ for example  'a' = 00, 'b' = 01 $latex \\ldots$ 'z' = 25. Once the plaintext is represented by numeric codes the ciphertext is generated as

| $latex
| c = x^e ~ \\text{mod(n)}
| $

| The receiver decrypts the ciphertext using modulo exponentiation operation with private key pair as
| $latex
| y = c^d ~ (\text{mod n})
| $

The decryption works as follows:

$latex y = x^{de} ~(\text{mod n})$

$latex y = x^{(1 + k\phi(n))} ~(\text{mod n})$

Now according to the Fermat's Little theorem,  for any integer x and prime number p (which is not a factor of x), $latex x^{p - 1} \\equiv 1 (\text{mod p})$ . Also by definition of the Euler's function $latex \\phi(pq) = (p - 1)(q - 1)$. Thus

$latex x^{(1 + k\phi(n))} \\equiv x ~(\text{mod p})$

This is true even when $latex x \\equiv 0 ~(\text{mod p})$. Following similar argument for the prime number q,

$latex x^{(1 + k\phi(n))} \\equiv x ~(\text{mod q})$

Combining above two equations according to the Chinese Remainder Theorem, we get

$latex x^{(1 + k\phi(n))} \\equiv x ~(\text{mod pq})$.

Hence $latex y = x^{de} = x ~(\text{mod n})$

( A complete explanation is available in the original `paper <http://securespeech.cs.cmu.edu/reports/RSA.pdf>`__ )

As a second part of the project, I implemented a simple version of RSA algorithm in Python . The program can generate an RSA public and private key pair, encrypt a plaintext string and recover original message from the ciphertext. The keys generated are eight digits long.  The plaintext can be a string ( Roman alphabets only for now, no special characters ). The program can be downloaded `here <https://github.com/sauravrt/CryptRSA>`__.
