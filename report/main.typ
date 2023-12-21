#import "template.typ": *

// From template.typ
#show: project.with(
  title: "Fuzzy Control",
  subtitle: "Uncertainty Modelling Coursework",
  authors: (
    (name: "Jonathan Raines", email: "jr0278@bristol.ac.uk"),
  ),
  date: "December, 2023",
)



= Introduction
Lofti Zadeh proposed Fuzzy Control in 1965 @zadeh_fuzzy_1965. It then gained popularity in Japan in the 1980s due to interest from large corporations such as Matsushita Electric Industrial Co and Hitachi and investment from the Japanese government through the founding of the Laboratory for International Fuzzy Engineering (LIFE). Its use in industrial and consumer applications is now widespread. In this report, I outline Fuzzy Control's advantages and overview its workings. I also examine the Control of an autonomous underwater vehicle as a case study for fuzzy Control. Finally, I compare Fuzzy Control to Statistical-Based Methods. 

= Motivation
*Intuitive:* Fuzzy Controllers are very interpretable. Control rules tend to follow the form of "If [property] then [action]". This format means experts can use their understanding of a system to write controllers naturally. Engineers can also debug controllers and verify they are working. Interpretability allows for reuse; engineers can modify existing controllers to work on new systems by making minimal changes rather than starting from scratch each time. Some have referred to Fuzzy Fuzzy Controllers as 'grey-box' as they balance 'black-box' systems like neural networks and 'white-box' _*First-Order Logic*_ (which are very interpretable but less concisely expressive).

*Efficiency:* Engineers have implemented fuzzy rules for Control in parallel hardware. The resulting systems are high-speed and use only a few kilobytes of memory. Many industrial applications require high-speed Control and are implemented on microchips with limited memory, making Fuzzy Control an ideal match. 

* Non-linear:* The _* transfer function* _ of a system maps its inputs to its outputs. In many use cases, it is non-linear, preventing the use of a classical control solution. Fuzzy Controllers allow discrete outputs (singletons), or piece-wise collections of linear functions, to be blended smoothly by allowing an input signal to be characterised both as, say, "somewhat low-pressure" and "somewhat nominal-pressure" where each option has a different output. In other words, Fuzzy Controllers approximate non-linear functions by combining simple rules. 

*Robust:* Fuzzy Controllers are often used for autonomous vehicles or industrial processes because they are fault tolerant. Performance may be affected if an input signal degrades or stops altogether, but the controller can still produce an output. 

Fuzzy Control systems do have drawbacks. One criticism is that no explicit model of the system being controlled exists. As a result, traditional control tools like stability analysis cannot be used to verify Fuzzy Controllers.

= Overview
Fuzzy Control has three main steps: fuzzification, inference, and defuzzification. 

== Fuzzification
Input values are often "crisp", for example, "pressure = 1012 mb". The first step in using them in a Fuzzy Controller is to convert them to fuzzy values. The controller assesses the input value's membership to each _*reference fuzzy set*_ in an appropriate _*partition*_. In this case, the partition consists of the"low-pressure, nominal-pressure, and high-pressure"  sets mentioned previously. The number of sets in a partition is called the _*granularity*_ and is typically between three and seven (a nominal value with one, two, or three categories on either side).

== Inference
The controller maps the input values $chi$ to the outputs $y$.

#align(center)[
  $S: chi subset R^n => y R^m $
]

=== Rule-based
*Linguistic:* Rules are written in the form "If [input] is [value], then [output] is [value]", sometimes referred to as _* Extended Modus Ponens*_. Modus Ponens (from Latin, meaning "method of affirming") is a term from _*Propositional Logic*_. Linguistic controllers are an extension of this principle as the _*antecedent*_ (the "If [input]" part) can be valid to an extent rather than just true or false. These systems are the most interpretable. However, a rule must be specified for each combination of outputs to input, so the number of rules grows exponentially with model inputs and outputs. Linguistic controllers are sometimes called Mamdani controllers, named after their creator @mamdani_experiment_1975. 

*Relational:* This type of controller maps the input fuzzy sets $A$ (made up of linguistic labels) to the output fuzzy sets $B$ (also linguistic labels) with a fuzzy relation.

E.g. $A$ = {Cold, Nominal, Hot}, $B$ = {Low Power, Medium Power, High Power}. The relation is then a set of weights. $r_"cold-LP"$, $r_"cold-MP"$, etc.

Relational controllers are a generalisation of the Linguistic model. The linguistic model rules are relations with one-hot vectors as relations. 

*Tokagi-Sugeno:* In this style of controller, rules are in the form "If $x$ is $A$ then $y_i = f(x_"i")$". It is a variant of a Relational controller, but rather than mapping inputs to another lexical term that can be defuzzified, they map to a linear function. The result is a blend of linear functions that together approximate the required overall non-linear control function. The drawback to this approach is that it loses some of the interpretability of Linguistic models. Especially as the controller's transfer function can better model the system's behaviour if the individual rule functions do _not_ approximate the true function locally @babuska_applied_1994.

=== Hybrid
Fuzzy Controllers can be combined with other control techniques. For example, REF is an example of using a Fuzzy Controller to modify the gains of a PID controller. 
//TODO 
== Defuzzification
The output of a controller needs to be crisp. In the pressure example, the output could be a valve position to regulate pressure, or in an anti-lock braking system, the output could be the breaking force. Defuzzification is the process of converting the fuzzy output of the fuzzy inference into a usable crips value. 

*Centroid:* The defuzzification rule outputs the "centre of mass" of all the fuzzy outputs from rules relating to the output variable. 
#align(center)[
$y_i = (integral_(x_"min")^(x_"max") mu_(B_i)(x_i).x_i dif x)/(integral_(x_"min")^(x_"max") mu_(B_i)(x_i) dif x)$
]

Where $mu_(B_i)()$ is the membership function for the $i^"th"$ set/lexical label in a partition of the output. E.g. $B_1$ is "low break pressure", $B_2$ is "nominal break pressure", etc.
This is often approximated with the discrete version @babuska_overview_1996.
#align(center)[
$y_i = (Sigma_(q=1)^(N_q) mu_(B_i)(x_i).x_i)/(Sigma_(q=1)^(N_q) mu_(B_i)(x_i))$
]

Where $N_q$ is the number of discretisation steps across the range, essentially, the $x_i$ is sampled $N_q$ times, and the products of those samples times their membership to the output label is divided by the sum of their memberships. This is the most commonly used defuzzification rule.

*Mean of Maximum:* A "winner takes all" approach. The defuzzifier returns the "nominal" value of the lexical label that has the highest membership. By nominal value, I mean $x$ for which $x$'s membership to output lexical label $B$ is 1, $mu_B (x)=1$.

*Centre of Maximum:* A weighted average version of Mean of Maximum. The defuzzifier returns a weighted average of the nominal values, using the membership for each label as a weight. 

= Applications
Engineers have used Fuzzy Control for a wide range of applications. A cement kiln in Denmark in 1978 was the first industrial application @martin_larsen_industrial_1980. The controller replaced a human operator; it controlled the rate at which coal was fed into the kiln and the amount the outlet vent was open based on parameters measured inside the kiln.

To provide context to the Overview in the previous section, I'll use the example of autonomous Control of marine vehicles @braginsky_obstacle_2016. In this paper, Braginsky and Guterman create an obstacle avoidance system for the BlueFin autonomous underwater vehicle. Their inputs come from a horizontal sonar sweep, as well as the target bearing for the vehicle. They divide the arc of the sonar sweep into nine radial arcs (section 5 being straight ahead). Each arc is evaluated for two input variables. The "safeness" of an arc is how close a path takes the BlueFin to an obstacle, and "remoteness" is how from the target heading an arc is. The input variables each have four reference fuzzy sets, e.g. "very safe", "safe", "risky", and "very safe". The authors use a relational controller (using the Łukasiewicz intersection) to find a direction that is both safe and not remote. The controller's output is the angle at which the rudder should steer the craft. Interestingly, they used smooth membership functions for "safeness" and "remoteness" given by $1/(1-e^(5-x))$. 
#figure(
  image("graph.svg", height: 4cm),
  caption: [
    A smooth membership function. y = $mu(x)$
  ],
)

= Comparison to Statistical-Based Approaches
There is a lot of overlap between Statistical-Based approaches and Fuzzy Control. In the Fuzzification step, evaluating the membership of an input to a reference fuzzy set $B$, $mu_B (x)$ is equivalent to the conditional probability $P(B|x)$. The inference step in Fuzzy Control produces a fuzzy output with many parallels with a probability distribution. For Statistical-Based controllers, the output value is the Expected Value of that distribution given by $f(z) = Sigma_1^r P(k|x).f_k (z) $ where $f_i$ represents a probability density function for the $k^"th"$ possible action (of $r$ total actions) available to the controller (outputs). This is equivalent to the "Center of Maximum" weighted average Defuzzification rule. Whilst the underlying maths can be similar, the formation of the approaches differs. Fuzzy Control is a knowledge-based approach. Experts define membership functions and rules. Its strength lies in allowing these experts to write expressive rules whilst handling vagueness. In contrast, probability is a data-driven approach. The conditional probabilities and probability density functions need to be generated from observations. As such, Fuzzy Control can be helpful when a large enough data set is unavailable. 

#pagebreak()

#bibliography("Fuzzy Control.bib", style: "bristol-university-press")