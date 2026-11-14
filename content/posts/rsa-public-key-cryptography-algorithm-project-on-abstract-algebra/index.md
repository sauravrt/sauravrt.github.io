+++
title = "RSA: Public Key Cryptography Algorithm (Project on Abstract Algebra)"
date = 2011-12-26T20:31:00
description = "A number-theory class project exploring RSA key generation, encryption, and decryption."
slug = "rsa-public-key-cryptography-algorithm-project-on-abstract-algebra"
aliases = ["rsa-public-key-cryptography-algorithm-project-on-abstract-algebra/"]
draft = false
[taxonomies]
tags = ["mathematics", "programming", "python"]
[extra]
legacy_source = "rsa-public-key-cryptography-algorithm-project-on-abstract-algebra.rst"
math = true
+++
> Archive note: this is a historical educational implementation, not a
> cryptography library suitable for real-world security.

Abstract Algebra was one of the mathematics courses I took for the Fall semester which has just ended. The complete course has two parts taught over two semesters. I took the first part and it mainly covered some basic Number Theory and largely Group Theory. As a part of the project I had to do a class project and my choice was RSA: A Public Key Cryptography Algorithm. The strength of RSA is based on difficulty in factoring large integers, specially those formed as product of two integers. The algorithm uses Number Theory concepts of modulo exponentiation, the Euler's function and the decryption is based on Euler's theorem. My objectives were to study the algorithm itself and do a simple implementation.

In public key cryptography, the key has a *public part* and a *private part*. The public part is made known to everybody whereas the private part is kept secret by the receiver (my PGP [public key](http://sauravtuladhar.info/pgp-public-key/)). Anyone who intends to send a message to the receiver encrypts the plaintext using the public key corresponding to the receiver. Once encrypted using the public key, the ciphertext can only be decrypted using the private key, which is safe with the receiver.

RSA is a public key cryptography algorithm jointly developed by R. Rivest, A. Shamir and L. Adleman and it was described in a [paper](https://doi.org/10.1145/359340.359342) in 1978. The name of the algorithm comprises the first letters of the three authors' surnames. The algorithm was originally patented by M.I.T. but was released to public domain in September 2000. The algorithm has three steps: (1) Key generation (2) Encryption (3) Decryption.

## Key generation

The RSA key pair is generated as follows:

- Generate a pair of prime numbers \\(p\\) and \\(q\\).
- Compute \\(n = pq\\).
- Compute the Euler's function \\(\phi(n) = (p - 1)(q - 1)\\).
- Find an integer \\(e\\) such that \\(1 < e < \phi(n)\\) and is coprime with \\(\phi(n)\\), i.e. \\(\gcd(e,\phi(n)) = 1\\).
- Find another integer \\(d\\) such that \\(de \equiv 1 \pmod{\phi(n)}\\). This is determined using the extended Euclidean algorithm which gives \\(ed + k\phi(n) = 1\\) where \\(k\\) is some integer.

The public key consists of the pair \\((e,n)\\) and the private key consists of the pair \\((d,n)\\).

## Encryption and decryption

RSA algorithm uses modulo exponentiation operation for both encryption and decryption. The plaintext is first converted to numeric codes. For instance, the letters in the plaintext are represented as integers \\(x\\), for example 'a' = 00, 'b' = 01, \\(\ldots\\), 'z' = 25. Once the plaintext is represented by numeric codes the ciphertext is generated as

\\[c = x^e \pmod n.\\]

The receiver decrypts the ciphertext using modulo exponentiation with the private key pair:

\\[y = c^d \pmod n.\\]

The decryption works as follows:

\\[y = x^{de} = x^{1 + k\phi(n)} \pmod n.\\]

Now according to Fermat's Little theorem, for any integer \\(x\\) and prime number \\(p\\) (which is not a factor of \\(x\\)), \\(x^{p - 1} \equiv 1 \pmod p\\). Also by definition of Euler's function \\(\phi(pq) = (p - 1)(q - 1)\\). Thus

\\[x^{1 + k\phi(n)} \equiv x \pmod p.\\]

This is true even when \\(x \equiv 0 \pmod p\\). Following a similar argument for the prime number \\(q\\),

\\[x^{1 + k\phi(n)} \equiv x \pmod q.\\]

Combining the above two equations according to the Chinese Remainder Theorem, we get

\\[x^{1 + k\phi(n)} \equiv x \pmod{pq}.\\]

Hence \\(y = x^{de} = x \pmod n\\).

A complete explanation is available in the [original paper](https://doi.org/10.1145/359340.359342).

As a second part of the project, I implemented a simple version of RSA algorithm in Python. The program can generate an RSA public and private key pair, encrypt a plaintext string and recover the original message from the ciphertext. The keys generated are eight digits long. The plaintext can be a string (Roman alphabets only for now, no special characters). The program can be downloaded from [CryptRSA on GitHub](https://github.com/sauravrt/CryptRSA).
