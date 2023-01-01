# Donald Knuth reward checks: how are distributed world wide?

An analysis of the distribution of the Donald Knuth reward checks in the world.

The [account balances](https://www-cs-faculty.stanford.edu/~knuth/boss.html) do not contain the country of the contributors.

Inferring a country from a person name is not a well posed problem, what should be the country? The native one? The one where the person lives most of his/her life?

Anyway, in order to get some insights, I relied on Philippe Remy's [`Name Dataset`](https://github.com/philipperemy/name-dataset) to get an estimate of the country related to a person (unfortunately I do not have an account at ChatGPT ;-).

There are a lot of intricacies to sort out in order to get a decent estimation, take for example the topmost contributor Udo Wermuth: according to Name Dataset, Udo can be a German first name but also a Nigerian last name.

So, I choose a very simple rule: I tokenize the contributor name, only one token should be classified as a last name, `and` all the token countries should be equal `and` all the token genders should be equal.

Unfortunately this rule leaves out more the 90% of the contributors, even the topmost Udo Wermuth is not included because, according to Name Dataset, Udo is associated with Germany while Wermuth is associated with Switzerland.

But for the remaining 87 contributors over the total of 910 I think that Name Dataset did a very good job (apart from a couple of blunders); you can get the results running [the pyhon script](./knuth_reward_check.py).




## Countries ranked by number of contributors (only 87 contributors over 910)

| country                   | contributors |
|:--------------------------|----------:|
| United States             |        27 |
| France                    |        11 |
| Germany                   |         9 |
| Italy                     |         9 |
| Japan                     |         6 |
| United Kingdom            |         5 |
| Iran, Islamic Republic of |         3 |
| Poland                    |         3 |
| Greece                    |         3 |
| India                     |         2 |
| Finland                   |         2 |
| Netherlands               |         2 |
| Slovenia                  |         1 |
| Russian Federation        |         1 |
| Spain                     |         1 |
| Czechia                   |         1 |
| Norway                    |         1 |

## Countries ranked by amount of hex dollars (only 87 contributors over 910)

| country                   | 0x$      |
|:--------------------------|:---------|
| Russian Federation        | 0x$80.00 |
| Germany                   | 0x$42.a0 |
| France                    | 0x$42.00 |
| United States             | 0x$28.a0 |
| Iran, Islamic Republic of | 0x$27.80 |
| Italy                     | 0x$10.a0 |
| United Kingdom            | 0x$9.a0  |
| Japan                     | 0x$9.80  |
| Poland                    | 0x$4.80  |
| Greece                    | 0x$4.20  |
| Finland                   | 0x$3.00  |
| India                     | 0x$3.00  |
| Netherlands               | 0x$2.00  |
| Czechia                   | 0x$1.20  |
| Norway                    | 0x$1.00  |
| Slovenia                  | 0x$1.00  |
| Spain                     | 0x$1.00  |