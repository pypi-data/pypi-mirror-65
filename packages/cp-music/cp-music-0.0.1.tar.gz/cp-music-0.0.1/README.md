## cp-music

A small library for constraint programming with `.musicxml` files in python using ortools (google's operation research library).

[![Build Status](https://travis-ci.org/CorbinMoon/cp-music.svg?branch=master)](https://travis-ci.org/CorbinMoon/cp-music)

refer to `/examples` directory for code examples

### Limitations
The music xml parser in this library does not currently support `<backoff>` tags and multi-part scores (scores with multiple instruments).
All notes comprising a chord must have separate voicings.