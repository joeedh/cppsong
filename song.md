# Undefined Behavior Blues

*(to the tune of a honky-tonk lament)*

**Verse 1**
I wrote a little program, just to add up one plus one,
Signed integer overflow — now my program's on the run.
The compiler looked at my code and just began to laugh,
"That's UB, my friend, I'll optimize your whole class in half!"

**Chorus**
Oh, undefined behavior, undefined behavior blues,
It compiles clean, runs fine on Tuesdays, crashes when you choose.
The standard says "not specified," the standard don't care why,
My nasal demons flew away and now my cat can fly.

**Verse 2**
I asked for move semantics, they said "it's an optimization,"
Then rvalue references gave me an identity crisis-nation.
I read the cppreference page for `std::launder` one more time,
Three years later, still don't get it, but I nod like it all makes sense in rhyme.

**Chorus**
Oh, undefined behavior, undefined behavior blues,
Whatever you meant, dear standard, I'm afraid I gotta lose.
I dangled a reference, I aliased through a `char*`,
Now Valgrind's screaming at me like I robbed a candy cart.

**Bridge**
Template error messages, forty pages tall,
"No matching function found" — didn't even try at all!
`std::enable_if`, SFINAE, concepts came to save the day,
But now I need a PhD just to make `Foo<Bar>` compile, okay?

**Verse 3**
They added modules, coroutines, and ranges to the mix,
Every three years a new standard, and none of my old code fits.
"Just recompile it," they tell me, "it's backwards compatible, see!"
Narrator: it was not compatible — it took down all of QA.

**Final Chorus**
Oh, undefined behavior, undefined behavior blues,
Fifty ways to shoot your foot and every one's front-page news.
But I still love you, C++, you beautiful cursed machine,
Zero-cost abstractions and the fastest bugs I've ever seen!

*(spoken outro)*
"Warning: unused variable 'my_will_to_live'."
