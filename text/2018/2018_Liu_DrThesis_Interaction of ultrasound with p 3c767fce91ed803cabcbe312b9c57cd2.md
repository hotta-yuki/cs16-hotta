# 2018_Liu_DrThesis_Interaction of ultrasound with periodic structures and composite structures

# Interaction of ultrasound with periodic structures and composite structures

Jingfei Liu

- To cite this version:

Jingfei Liu. Interaction of ultrasound with periodic structures and composite structures. Other. Université de Lorraine, 2013. English. NNT: 2013LORR0329 . tel-01751151

HAL Id: tel-01751151
[https://hal.univ-lorraine.fr/tel-01751151](https://hal.univ-lorraine.fr/tel-01751151)
Submitted on 29 Mar 2018

HAL is a multi-disciplinary open access archive for the deposit and dissemination of scientific research documents, whether they are published or not. The documents may come from teaching and research institutions in France or abroad, or from public or private research centers.

L’archive ouverte pluridisciplinaire HAL, est destinée au dépôt et à la diffusion de documents scientifiques de niveau recherche, publiés ou non, émanant des établissements d’enseignement et de recherche français ou étrangers, des laboratoires publics ou privés.

## AVERTISSEMENT

Ce document est le fruit d’un long travail approuvé par le jury de soutenance et mis à disposition de l’ensemble de la communauté universitaire élargie.

Il est soumis à la propriété intellectuelle de l’auteur. Ceci implique une obligation de citation et de référencement lors de l’utilisation de ce document.

D’autre part, toute contrefaçon, plagiat, reproduction illicite encourt une poursuite pénale.

Contact : [ddoc-theses-contact@univ-lorraine.fr](mailto:ddoc-theses-contact@univ-lorraine.fr)

## LIENS

Code de la Propriété Intellectuelle. articles L 122. 4
Code de la Propriété Intellectuelle. articles L 335.2- L 335.10
[http://www.cfcopies.com/V2/leg/leg_droi.php](http://www.cfcopies.com/V2/leg/leg_droi.php)[http://www.culture.gouv.fr/culture/infos-pratiques/droits/protection.htm](http://www.culture.gouv.fr/culture/infos-pratiques/droits/protection.htm)

# THÈSE  pour l’obtention du titre de  Docteur de l’Université de Lorraine

Spécialité : Acoustique présentée par :

Jingfei Liu

# L’Interaction des ultrasons avec des structures périodiques et les structures composites

Thèse soutenue publiquement le 3 décembre 2013, à Georgia Tech Lorraine devant le jury compose de :
M. M. Deschamps
M. B. Dubus
M. J. P. Salvestrini
M. V. Laude
M. F. Meraghni
M. S. W. Yoon
M. A. Ougazzaden
M. N. F. Declercq

Directeur de recherche (LMP, UMR5469)
Directeur de recherche (IEMN, ISEN)
Professeur (Université de Lorraine)
Directeur de recherche (Institut Femto-ST)
Professeur (ENSAM)
Professeur (SungKyunKwan University, KR)
Professeur (UMI 2958 GT-CNRS)
Professeur (UMI 2958 GT-CNRS)

Rapporteur
Rapporteur
Examinateur
Examinateur
Examinateur
Examinateur
Co-directeur de thèse
Directeur de thèse

LUNE, 2, rue Marconi, Metz
Georgia Tech Lorraine, GT-CNRS UMI 2958

## AKNOWLEDGEMENTS

I wish to thank, first and foremost, my advisor, Professor Nico F. Declercq, for his professional guidance and valuable support during the past four years of my study at Georgia Tech Lorraine. I admire his scientific intuition and intellectual curiosity, and I am grateful for his scientific advices and insightful suggestions. I would also like to offer my special thanks to my co-advisor, Professor Abdallah Ougazzaden, for his great support for my pursuit of this degree. He is the person whom I can turn to for help at critical times, and I would not be able to come this far without his help.

I would like to express my very great appreciation to all of my jury members: Professor Marc Deschamps from Université Bordeaux 1, Professor Bertrand Dubus from IEMN (UMR 8520) ISEN, Professor Jean-Paul Salvestrini from Université de Lorraine, Professor Vincent Laude from Université de Franche-Comté, Professor Fodil Meraghni from ENSAM, and Professor Suk Wang Yoon from SungKyunKwan University (Republic of Korea). It is a great honor for me to have such a high level jury.

I wish to acknowledge the help provided by my former colleagues, Dr. Sarah W. Herbison and Dr. L. Satyanarayan and Dr. Rayisa Moiseyenko. They offered me many useful suggestions when I started my research in the ultrasonic lab. I would also like to thank my current lab peers Peter McKeon, Anurupa Shaw and Qi Wang and the technician Olivier. They share their ideas that are helpful to my work. I give my special thanks to Olivier who always unconditionally supports my experiments with his expertise in mechanics. I also want to thank my friends, Dr. Zheshen Zhang (a current Postdoctoral research at MIT), Ning Tian (a current Ph.D. student at Georgia Tech Atlanta), and Wei Ye (a current Ph.D. student at Georgia Tech Lorraine). I will never forget the many wonderful lunches and fun activities that we had together.

I wish to extend my thanks to the staff at Georgia Tech Lorraine. I really appreciate Josyane Roschitz for her continuous help in almost everything from academic issues to personal matters in the first two years of my residence in France. The same appreciation is also given to Isabelle Hindre, Corinne Guyot and Katia Menard for their help with my current stay in France. Thanks to Jean-Jacques Michel for his help in solving our computer and Internet problems, especially in the urgent situations. My gratefulness is also given to Laetitia Richert for her efforts in dealing with all my CNRS related activities. I am also thankful to our accountant Sandrine Cadamuro for her kindness and efficient work.

At last, I want to express my deepest gratitude to my family for their love, support, and encouragement throughout my doctoral study. I wish to thank my parents whom I have not been able to spend a lot of time with in the past year, and I deeply appreciate their understanding. I am also grateful to my beloved wife who is the great source of support in the hard times.

## TABLE OF CONTENTS

ACKNOWLEDGEMENTS ….. i
LIST OF TABLES ….. vi
LIST OF FIGURES ….. vii
SUMMARY ….. ix
I INTRODUCTION ….. 2
1.1 Ultrasonic Diffraction Effect on Periodic Surfaces ….. 2
1.2 Ultrasonic Characterization of Defects in Composite Plate ….. 4
1.3 Overview of this Thesis ….. 6
II ACOUSTIC WOOD ANOMALY PHENOMENON ….. 10
2.1 Introduction ….. 10
2.2 Samples and Experimental Setup ….. 12
2.3 Results and Discussion ….. 15
2.3.1 Observation of Spectral Anomalies ….. 16
2.3.2 Existing Explanations of Acoustic Wood Anomaly ….. 18
2.3.2.1 On mode conversion assumption ….. 18
2.3.2.2 On the assumption of energy loss ….. 22
2.3.2.3 On the assumption of finite beam effect ….. 26
2.3.2.4 On the assumption of surface resonance generation ….. 27
2.3.2.5 On the assumption of double mode conversion ….. 32
2.3.3 New Explanations of Acoustic Wood Anomaly ….. 35
2.3.4 Additional Experiments ….. 37
2.3.4.1 Spectral anomaly of brass-water interface ….. 38
2.3.4.2 Spectral anomaly of brass-air interface ….. 39
2.5 Conclusion ….. 41
III SUB-HARMONIC DIFFRACTION PHENOMENON ….. 44
3.1 Introduction ….. 44
3.2 Samples and Experimental Setup ….. 45
3.2.1 Samples ….. 45
3.2.2 Transducer Selection ….. 49
3.2.3 Experimental Setup and Procedures ….. 50
3.3 Perfect Diffraction ….. 52
3.3.1 Bragg Diffraction of Silicon Samples ….. 52
3.3.2 Theory based on Fourier ….. 54
3.4 Sub-harmonic Diffraction ….. 55
3.4.1 Bragg Diffraction of Silicon Samples ….. 55
3.4.2 Adjustment of Grating Equation to Incorporate Internal Reflection ….. 57
3.4.3 Bragg Diffraction of Brass Samples ….. 58
3.5 Discussion ….. 61
3.5.1 Wrong Fourier Theory ….. 62
3.5.2 Imperfect Periodicity ….. 63
3.6 General Diffraction Experiment ….. 64
3.7 Prediction of Sub-harmonic Diffraction in Optics ….. 66
3.8 Conclusions ….. 67
IV AIR-COUPLED ULTRASONIC INVESTIGATION OF STACKED CYLINDERICAL RODS ….. 70
4.1 Introduction ….. 70
4.2 Theoretical Considerations ….. 74
4.3 Samples and Experimental Setup ….. 74
4.3.1 Sample Preparation ….. 74
4.3.2 Transducer Selection ….. 75
4.3.3 Experimental Setup and Procedures ….. 78
4.4 Results and Discussion ….. 81
4.4.1 Calibration and Method for Data Extraction ….. 81
4.4.2 Method to Extract Bragg Angles for Different Frequencies ….. 83
4.4.3 Periodicity Evaluation Using Approach I ….. 84
4.4.4 Periodicity Evaluation Using Approach II ….. 86
4.4.5 Comparison between Direct Measurement and Ultrasonic Evaluations ….. 87
4.4.6 Robustness Investigation of the Applied Method for the Poor Quality 310 kHz Transducer ….. 87
4.5 Conclusion ….. 89
V ULTRASONIC GEOMETTRICAL CHARACTERIZATION OF PERIODICALLY CORRUGATED SURFACES ….. 92
5.1 Introduction ….. 92
5.2 Samples and Experimental Setup ….. 94
5.2.1 Samples ….. 94
5.2.2 Experimental Setup ….. 96
5.3 Dominating Factors of Characterization Quality ….. 98
5.3.1 Special Properties of the Transducer Beam ….. 98
5.3.1.1 Bandwidth and Spatial Resolution ….. 98
5.3.1.2 Central Frequency and Wavelength ….. 100
5.3.2 Ultrasonic Beam Diameter ….. 101
5.3.3 Spatial and Temporal Sampling Intervals ….. 107
5.3.4 Data Processing Methods ….. 108
5.4 Experimental Results and Discussions ….. 109
5.4.1 Characterization of the Lateral Corrugation Geometry ….. 109
5.4.2 Characterization of the Vertical Corrugation Geometry ….. 111
5.4.3 Comparison of the Results Obtained Using Different Techniques ….. 112
5.5 Conclusions ….. 114
VI CHRACTERIZATION OF IMPACT DEFECTS OF COMPOSITE PLATES ….. 117
6.1 Introduction ….. 117
6.2 Experiments ….. 118
6.2.1 Specimen ….. 118
6.2.2 Experimental Setup ….. 119
6.3 Data Processing ….. 119
6.3.1 Reflection Signals ….. 119
6.3.2 C-scan Representation ….. 121
6.3.3 Conventional Signal Property Extraction ….. 121
6.3.4 Spectral Signal Property Extraction ….. 122
6.4 Results and Discussion ….. 123
6.4.1 Conventional Characterization ….. 123
6.4.2 Spectral Characterization ….. 124
6.5 Conclusions ….. 127
VII COMPARISON OF DIFFERENT APPROACHES IN CHARACTERIZATION OF IMPACT DEFECTS OF COMPOSITE PLATES ….. 129
7.1 Introduction ….. 129
7.2 Experiments ….. 130
7.2.1 Sample Preparation ….. 130
7.2.2 Transducer Selection ….. 130
7.2.3 Experimental Configuration ….. 131
7.3 Data Processing ….. 132
7.3.1 Response Signals ….. 132
7.3.2 Time-Domain Data Analysis ….. 134
7.3.3 Frequency-Domain Data Analysis ….. 134
7.4 Results and Discussion ….. 135
7.4.1 TOF and Amplitude ….. 135
7.4.2 Time-Domain Attenuation ….. 136
7.4.3 Frequency-Domain Attenuation ….. 139
7.4.4 Effect of Transducer Type ….. 139
7.5 Conclusions ….. 140
VIII SUMMARY AND FUTHURE WORK ….. 143
8.1 Concluding Summary: The Investigation of the Interaction of Ultrasound with Periodic Structures ….. 143
8.2 Concluding Summary: The Investigation of the Ultrasonic Characterization of Impact Defects of Composite Plates ….. 145
8.3 Future for the Interaction of Ultrasound with Periodic Structures ….. 146
8.4 Future for the Characterization of Impact Defects of Composite Plate ….. 146

## LIST OF TABLES

Table 2-1 Summery of experimentally observed mode conversion at anomaly frequencies for different corrugated interfaces, profile, and velocity relationship. Here $c_{f}$ is the longitudinal wave velocity of fluid, $c_{R}$ the Rayleigh wave velocity, $c_{l}$ the longitudinal wave velocity, and $c_{s}$ the shear wave velocity of solid.

Table 2-2 Related wave velocities.
Table 2-3 Identification of converted modes at anomaly frequencies for the corrugated water-brass interface based on mode conversion theory.

Table 3-1 Dimensional parameters of the corrugated samples: corrugation periodicity ( $\Lambda$ ), corrugation height (H) and their relative average (A) and the ratio between standard deviation and average (SD/A), the ratio of corrugation periodicity to height ( $\Lambda / \mathrm{H}$ ), and the total thickness (T).

Table 3-2 Basic parameters of the immersion transducers used in this study.
Table 3-3 Values of all possible diffraction orders obtained based on experimental results and the classical grating equation for Silicon I.

Table 3-4 Values of all possible diffraction orders obtained based on experimental results and the classical grating equation for Brass I.

Table 4-1 Diameter averages and the corresponding standard deviations and ratios of standard deviation to average of the three sets of spaghetti rods.

Table 4-2 Comparison of the periodicity measurements of three samples obtained in direct measurement, Approach I at 220 kHz and Approach II at 220 kHz. ‘SD/A’ refers to the ratio of the standard deviation to the mean. ‘Difference’ refers to the percentage difference between the mean diameter obtained from the angular spectrogram and that obtained with the direct measurement.

Table 4-3 Comparison of the periodicity measurements of three samples obtained from the first order and second order Bragg angles in Approach I and Approach II using the 310kHz transducer. ‘SD/A’ and ‘Difference’ are defined in Table 5-2.

Table 5-1 Corrugation characteristic dimensions of the samples: the average value (A) and their respective ratio of standard deviation to average value (SD/A).

Table 5-2 Corrugation characteristic dimensions obtained from the ultrasonic images: average value (A) and the ratio of standard deviation to average value (SD/A).

Table 5-3 Difference of the corrugation characteristic dimensions obtained using ultrasonic techniques and those obtained using optical technique (E) and the percentage ratio of the difference to the periodicity $(\mathrm{E} / \Lambda)$.

## LIST OF FIGURES

Figure 2-1 Schematics of the experimental setup for obtaining reflections from periodically corrugated rectangular (a) water-brass interface and (b) brass-water and brass-air interfaces, and the setup of (c) polar scan of the diffraction field.

Figure 2-2 Comparison of the reflection spectra from flat and periodically corrugated water-brass interfaces: (a) shows the respective spectra of flat surface reflection and corrugated surface reflection; (b) is the amplitude difference between of the two spectra; and (c) is the ratio of amplitudes of the two spectra.

Figure 2-3 (a) B-scan and (b) angular spectrogram of diffraction field obtained from the periodically corrugated water-brass interface for normal incidence.

Figure 2-4 Comparison of the reflections from flat and periodically corrugated waterbrass interfaces in time domain and time-frequency domain: (a) shows the waveforms of the two reflections; (b) is the sonogram of the flat interface reflection; and (c) is the sonogram of the corrugated interface reflection.

Figure 2-5 Comparison of the main bang and the tail of the reflection from corrugated water-brass interface: (a) waveform and (b) amplitude spectrum of the main bang; (c) waveform and (d) amplitude spectrum of the tail.

Figure 2-6 Comparison of the phase spectra of the reflection from (a) flat and (b) corrugated water-brass interfaces.

Figure 2-7 (a) B-scan and (b) angular spectrogram of the oscillating tails of diffraction obtained from the periodically corrugated water-brass interface for normal incidence.

Figure 2-8 Comparison of the reflections from flat and periodically corrugated brasswater interfaces: (a) waveforms, (b) amplitude spectra, (c) sonogram of flat interface reflection, and (d) sonogram of corrugated interface reflection.

Figure 2-9 Comparison of the reflections from flat and periodically corrugated brass-air interfaces: (a) waveforms, (b) amplitude spectra, (c) sonogram of flat interface reflection, and (d) sonogram of corrugated interface reflection.

Figure 3-1 Images of the corrugation structures of the four silicon samples: (a) Silicon I, (b) Silicon II, (c) Silicon III and (d) Silicon IV.

Figure 3-2 Images of the corrugation structures of the three corrugated brass samples: (a) Brass I, (b) Brass II, (c) Brass III.

Figure 3-3 Schematics of experimental setup: (a) Bragg diffraction configuration and (b) general diffraction configuration.

Figure 3-4 Angular spectrogram of the Bragg diffraction field of (a) Silicon III and (b) Silicon IV obtained using a 20 MHz transducer.

Figure 3-5 Angular spectrogram of the Bragg diffraction field of (a) Silicon I and (b) Silicon II obtained using a 20 MHz transducer.

Figure 3-6 Angular spectrogram of the Bragg diffraction field of (a) Brass I, (b) Brass II and (c) Brass III obtained using a 20 MHz transducer.

Figure 3-7 Absolute values of all possible diffraction orders from -1 to +1 order of Bragg diffraction. The values are extracted based on experimental data and classical grating equation.

Figure 3-8 Angular spectrogram of the general diffraction field of (a) Silicon II with an incidence angle of -10° and a polar scan range of 30° to 90°, and (b) Brass I with an incidence angle of -30° and a polar scan range of -20° to 90° obtained using a 20 MHz transducer.

Figure 3-9 Simulation of the spatial diffraction spectrum of a white light normally incident onto a grating with a periodicity of 700 nm based on the classical grating equation.

Figure 3-10 Simulation of the spatial diffraction spectrum of a white light normally incident onto a grating with a periodicity of 700 nm: (a) diffraction of order 1/2; (b) diffraction of order 3/2; and (c) combination of the diffractions of order 1/2, 1 and 3/2.

Figure 4-1 Schematic of the diffraction pattern for an acoustic beam incident onto a periodic surface with a periodicity $\Lambda$. The incident beam, the beam of specular reflection (diffracted beam of zero order), the first positive order diffracted beam, the first and second negative order diffracted beams and their corresponding angles are shown.

Figure 4-2 Cross-sectional view of the three types of packing of rods.
Figure 4-3 Comparison of the angular spectrograms of the polar scans on a flat surface of (a) the 220 kHz transducer and (b) the 310 kHz transducer for the purpose of transducer quality evaluation. The minimum intensity is $1 / \mathrm{e}^{2}$ of the maximum value.

Figure 4-4 (a) Time waveform of the incident pulse of the 220 kHz transducer, and (b) its frequency spectrum.

Figure 4-5 (a) Time waveform of a typical reflected wave of the 220 kHz transducer, and (b) its frequency spectrum.

Figure 4-6 Scan range to detect the backscattered beam at Bragg-angles.
Figure 4-7 Angular spectrogram of the polar scan on a flat surface obtained using the air-coupled transducer with central frequency of 220 kHz. The characteristics of the angular spectrogram used for data reading such as diminutive fringes and major fringe are shown.

Figure 4-8. Angular spectrogram of the polar scan on the periodic surface composed of cylindrical rods with average diameter of (a) 1.385 mm, (b) 1.655 mm and (3) 1.915mm obtained using an air-coupled transducer of central frequency of 220 kHz .

Figure 4-9 Comparison of the Bragg angle-frequency values acquired in Approach I from their angular spectrograms and their theoretical expectations (bold line) for three sample periodic surfaces. For the frequency range of 210 to 225 kHz no Bragg anglefrequency values are available because of the existence of major fringes which blur the fringes.

Figure 4-10 Diameters of the construction cylindrical rods obtained based on Bragg angle-frequency values acquired in Approach I for three sample periodic surfaces.

Figure 4-11 Angular spectrogram of the polar scan on the periodic surface composed of cylindrical rods with average diameter of 1.915 mm obtained using a poor quality aircoupled transducer of central frequency of 310 kHz . A poor quality of the measured results is clear when compared to Figure 5-8 (c). Nevertheless it is possible to extract the diameter with relatively high accuracy.

Figure 5-1 Top and side views of the three corrugated brass samples: (a) and (b) are Sample I; (b) and (c) are Sample II; (e) and (f) are Sample III.

Figure 5-2 Reflections from the corrugated surfaces of (a) Sample I, (b) Sample II, and (c) Sample III.

Figure 5-3 Effects of beam diameter on the reflected echo energy. Image (a) is the schematics of the periodic corrugations for the simulation and the cross sections of four beams with different diameters. The lighter area is plateau and the darker area is valley. The value of $\mathrm{k}_{\mathrm{P}}$ is 35.9% (Sample II). Image (b) to (e) show the normalized energy levels of plateau reflection, valley reflection and ideal plateau reflection for the four cases shown in (a) from left to right respectively. The beam diameter is $0.8 \Lambda_{\mathrm{P}}$ or $0.287 \Lambda$ for (b), $2 \Lambda_{\mathrm{P}}$ or $0.718 \Lambda$ for (c), $2.4 \Lambda_{\mathrm{P}}$ or $0.862 \Lambda$ for (d), and $\Lambda$ for (e).

Figure 5-4 Effects of beam diameter on characterization accuracy of plateau width $\Lambda_{\mathrm{P}}$ for five corrugations with different $k_{p}$. In this study Sample I has a $k_{P}$ value of $40.5 \%$, Sample II 35.9% and Sample III 23.2%.

Figure 5-5 The images characterizing Sample II based on (a) the difference between the maximum amplitude of the plateau reflection and that of the valley reflection and (b) the TOFs to the peaks with maximum amplitude.

Figure 5-6 The images characterizing Sample III based on (a) the difference between the maximum amplitude of the plateau reflection and that of the valley reflection and (b) the TOFs to the peaks with maximum amplitude.

Figure 5-7 The distance between the transducer surface and the scanned surface at the index position of 2 mm obtained based on the TOFs to the peaks with maximum amplitude for (a) Sample II and (b) Sample III.

Figure 2-8 Comparison of the average values of the measurements for Sample II and III obtained with optical microscopic technique and the ultrasonic techniques using amplitude and TOF.

Figure 6-1 (a) Optical image and (b) ultrasonic image of the scanned area of the specimen.

Figure 6-2 Comparison of the reflections from unimpacted area and impacted area in (a) time domain and (b) in frequency domain.

Figure 6-3 Spectrum of the reflection signal windowed from $38.5 \mu \mathrm{~s}$ to $39.6 \mu \mathrm{~s}$.

Figure 6-4 (a) B-scan of the reflection signals windowed from $38.5 \mu \mathrm{~s}$ to $39.6 \mu \mathrm{~s}$ at the index position of 15 mm and (b) its spectral representation.

Figure 6-5 C-scan images obtained based on (a) the maximum amplitude, (b) the minimum amplitude, (c) the TOF to the peak with maximum amplitude, and (d) the TOF to the trough with minimum amplitude of the windowed reflections.

Figure 6-6 C-scan images obtained based on the amplitudes of the frequency components at (a) 5 MHz, (b) 10 MHz, (c) 15 MHz, (d) 20 MHz, (e) 25 MHz, (f) 30 MHz, (g) 35 MHz, and (h) 40 MHz.

Figure 7-1 Schematic of pseudo pulse-echo mode at the critical angle $\theta_{c}$.

Figure 7-2 Absolute amplitude of transmitted wave through the sample plates at different indent angles.

Figure 7-3 Comparison of response signals at unimpacted area and impacted area for (a) pitch-catch mode, (b) pulse-echo mode and (c) pseudo pulse-echo mode.

Figure 7-4 Comparison of the spectrums of response signals at unimpacted area and impacted area for pitch-catch mode.

Figure 7-5 Comparison of the effects of amplitude and TOF in characterizing the impact defect for Sample 1. (a), (b) and (c) are respectively the amplitudes of absolute values, maximum peaks and negative peaks of the first response wave at each position; (d), (e) and (f) are respectively the TOFs to negative peaks, positive peaks and preset threshold.

Figure 7-6 Comparison of the amplitude sensitivity to impact defects of the first wave and the second wave in pitch-catch mode. (a) and (b) are respectively the amplitudes of the maximum peaks and minimum peaks of the first wave; while (c) and (d) are those of the second waves.

Figure 7-7 Comparison of the amplitude sensitivity to impact defects of the signal in the interval between the first two waves in (a) pulse-echo mode and (d) pseudo pulse-echo mode and the second wave in (a) pulse-echo mode and the first wave in (b) pseudo pulse-echo mode.

Figure 7-8 Comparison of the responses of maximum amplitude to the impact defects in pitch-catch mode at different frequency components: (a) 1.98 MHz, (b) 2.67 MHz, (c) 3.30 MHz, (d) 3.93 MHz, (e) 4.58 MHz and (f) 5.25 MHz.

Figure 8-1 An aluminum block with holes of different diameters.

Figure 8-2 (a) B-scan of the reflections from the designed holes and (c) its frequency domain representation.

## SUMMARY

The research on the interaction of acoustic waves and periodic structures or surfaces has a long history that can be dated back to the time of Lord Rayleigh. However, most of the research in this area has been done in the last three decades possibly due to the advances in research facilities for both numerical simulation and experimental investigation. In this thesis the investigation in this area is continued in two aspects: study of the physical phenomenon of ultrasound diffraction and study of the nondestructive characterization of corrugated structures using ultrasonic techniques. Chapter II and III present the investigation of two physical phenomena of ultrasound diffraction, i.e. acoustic Wood anomaly and the so-called sub-harmonic diffraction, respectively. In Chapter IV the principle of Bragg diffraction is applied to the measurement of the periodicity of periodic structures using air-coupled ultrasonic technique; while a more general geometrical characterization of periodic surface using high frequency ultrasonic C-scan imaging technique is presented in Chapter V.

The research work of the interaction of ultrasound with composite structures presented in this thesis focuses on the characterization of impact defects of composite plates. This work contains two parts: the spectral analysis of impact defects and the comparison of different techniques in impact defects characterization. The first part of the work tries to deal with the situation where the received signals for defect characterization are corrupted by avoidable high-level noise caused by the data acquisition system. While in the second part of this work different testing configurations, different transducers and different data processing methods are compared in order to find the best possible way for the defect characterization.

## RESUME DU CHAPTRE I

Ce chapitre sert d’introduction aux deux catégories de travaux de recherche présentés dans cette thèse: l’interaction des ultrasons avec des structures périodiques et l’interaction des ultrasons avec des plaques composites. Les motivations générales et axes de travaux de recherche respectifs y sont présentés. Ainsi que le plan du manuscrit.

## CHAPTER I INTORDUCTION

### 1.1 Ultrasonic Diffraction Effect on Periodic Surfaces

The study of acoustic diffraction on periodic surfaces was initiated by Lord Rayleigh [1] more than one hundred years ago, but after that the research progress in this area had been very slow till late 70’s and early 80’s of last century. The increase in the research of ultrasonic diffraction effect on periodic surfaces possibly results from the increasing calculation power, which enables more complicated calculations for numerical simulation, the development of ultrasonic spectrographic technique, and the improvement of experimental capability, which make more sophisticated experimental investigations possible.

The motivation of studying the interaction between ultrasound and periodic structures arises partially from the general interest in the physical mechanism involved, and more from the possibility of the generation of Scholte-Stoneley wave by surface corrugation [2-4]. Theoretically, different from the generation of Rayleigh surface wave the Scholte-Stoneley wave is impossible to be generated on smooth surfaces, but due to the diffraction effect the incident bulk wave is possible to couple with the corrugated interface and the Scholte-Stoneley wave can accordingly be generated on corrugated surfaces through mode conversion process. At the same time, Rayleigh wave can also be generated on corrugated surfaces through a similar physical process. The generation of these surface-type waves promises their potential application in nondestructive testing/evaluation of both corrugated surfaces and the smooth surfaces such as characterizing the interfaces of layered materials and the quality of their bonding [5]. The possibility of generating surface acoustic waves on the corrugated surface also make it possible to design a new type of transducer or sensor on solids for signal processing
[6,7], especially on non-piezoelectric solids for which the conventional method of surface wave generation using inter-digital transducers is impossible.

In the study of the interaction of ultrasound with periodic surfaces physical phenomena such as backward displacement [8-12] and Wood anomaly [13-17] have been observed and studied. Although the occurrence of all these physical phenomena is widely believed to be related to the generation of surface-type waves on the corrugation, their corresponding theoretical explanations and assumptions still need more support from further investigations, especially from experimental investigations. In this thesis the physical origin of acoustic Wood anomaly is investigated and this investigation is focused on obtaining a better understanding of the physical mechanism of this phenomenon based on new experimental investigations.

Although the classical grating equation is originated from optics, it is the rule of thumb in explaining the ultrasonic diffraction effects on periodic surfaces. This equation describes the relationship between the directions of the diffracted waves of different orders and their corresponding frequencies for a given incident angle and a grating with a given periodicity. A lot of experimentally observed phenomena of ultrasonic diffraction can be satisfactorily explained by the classical grating equation, but there are some exceptions such as the so-called sub-harmonic diffraction phenomenon observed and studied in this thesis. In the classical grating equation the periodicity refers to the smallest identifiable periodicity, i.e. the fundamental periodicity, of a given corrugation, and neither a fraction of the fundamental periodicity nor a multiple of it has been considered to be applied in the equation. However, in this thesis it is shown that the experimentally obtained diffraction fields go beyond what the classical grating equation is capable of explaining, and an extended grating equation, in which a multiple of the fundamental periodicity is considered, has to been introduced in order to successfully
explain the experimental observations.
The study of the diffraction effect of ultrasound on periodic surfaces has many potential applications including nondestructive testing/evaluation of the periodically corrugated surfaces themselves. For example, ultrasonic Bragg scattering as a typical acoustic diffraction effect has been applied to characterize the corrugation periodicity of periodically stacked cylindrical rods [18] under the scope of air-coupled ultrasonics. Actually, the principle of this work is applicable to all the similar cases and the most challenging application is in air-coupled ultrasonics. In addition, the diffraction effect should, in some cases, be avoided in nondestructive characterization of corrugated structures because it may result in decrease in characterization accuracy or even makes the task impossible.

### 1.2 Ultrasonic Characterization of Defects in Composite Plate

Composite materials are widely used in almost all branches of modern industries and everyday life. Among all the geometrical forms of composite materials, composite plate is probably the most widely used form. The biggest challenge in the practical application of composite plates is the potential damage caused by their inner defects. There are a variety of physical mechanisms that could possibly cause inner defects in composite plates, and impact is one of them. Nondestructive characterization of impact defects of the composite plates is of great interest in the quality control during the manufacturing process and in the safety monitoring in practical applications. Among many nondestructive methods that are available for this purpose, immersion (water-coupled) ultrasonic testing is a good choice because of its low cost, high reliability and efficiency. The research work in the investigation of the interaction between ultrasound and
composite structures presented in this thesis focuses on the characterization of the designed impact defects of composite plates.

The basic concerns in the impact defect characterization for composite defects are the location/position, shape, size of the defects in lateral plane of the plates, the depth and size of the defect in the vertical direction of the plates, the severity and type of defects, etc. It is ideal to obtain all the above information of one specific defect from a signal test, but it is very challenging in practice. The lateral defect properties such the defect location, shape and size, which are the focus in most characterization research, are relatively easy to characterize, but the vertical defect properties are relatively difficult to characterize. If the results of characterization are represented as images of the lateral plane of the tested samples, defect severity can normally be shown by the color intensity or the contrast. As to the type of defects, it is really hard to determine from the obtained signals.

In practical situations there are many challenges in ultrasonic impact defect characterization such as the existence of high-level noises in the received signals, limitation in testing configuration available, lack of transducers with proper frequency, mismatch between the received signals and the corresponding data processing methods, etc. It is hard to address the possible solutions for all these challenges, and therefore, only two situations are dealt with in this thesis. The first situation investigated in this thesis is the case in which the received signals are corrupted by high-level noises. Denoising has been widely studied in almost all branches of scientific research and many theories and corresponding techniques have been proposed for different situations, but there is no universal technique for every situation. In this work we only study the data processing in frequency domain. The other project that has been investigated and presented in this thesis is trying to compare different techniques of immersion ultrasonic
characterization of impact defects for obtaining an optimized combination of testing configuration, transducer selection and data processing method. Through this effort we aim to find the better matching between different factors that affect the final results of the characterization.

### 1.3 Overview of This Thesis

The research work presented in this thesis fall into two categories: (i) interaction of ultrasound with periodic structures and (ii) interaction of ultrasound with composite structures.

Under the category of the interaction of ultrasound with periodic structures two physical phenomena of diffraction effect are discussed first. The first physical phenomenon of diffraction investigated is the so-called acoustic Wood anomaly. This phenomenon refers to the spectral anomalies, sharp dips or tips, appearing in the spectrum of the reflection from corrugated surface when a broadband sound beam is normally incident onto the surface. An analogous phenomenon exists in optics and it has been studied intensively in the last century. But due to the difference of nature between mechanical wave and electromagnetic wave, the study in optical Wood anomaly cannot be fully transferred to acoustic Wood anomaly. Therefore, an individual investigation of acoustic Wood anomaly has to be made and the work in this thesis focuses on its physical origin. All the existing theories concerning the physical origin of acoustic Wood anomaly have been first reviewed, and then analyzed and evaluated based on the experimental investigation performed in this work. And a relatively complete physical explanation is given for this phenomenon. All the details of this investigation are presented in Chapter II.

The second physical phenomenon of diffraction investigated is a sub-harmonic diffraction effect. The experimental observation and the corresponding theoretical discussions are presented in Chapter III. Normally, the angle-frequency patterns of an incident broadband ultrasound beam diffracted by a corrugated surface can be successfully explained using the classical grating equation. However, diffraction patterns existing in between those predicted by the classical grating equation were experimentally observed from the diffraction field of corrugated silicon samples and the classical grating equation is incapable of explaining them. The physical origin of this observation is discussed and its counterpart possibly existing in optics is predicted through numerical simulation.

Diffraction effect can also be useful in nondestructive testing. As an example, the application of acoustic Bragg diffraction to the measurement of corrugation periodicity of stacked cylindrical rod using air-coupled ultrasonic technique is presented in Chapter IV. The significance of this work is that the measurements are highly accurate although only cheap and low quality air-coupled transducer is used. And due to the robustness and accuracy of the proposed technique it promises wide industrial applications.

Diffraction effect is not always desired in nondestructive testing such as the case presented in Chapter V. In this work the frequency of ultrasound is chosen to be high enough to avoid diffraction effect caused by surface corrugation in order to obtain quantitative evaluation of the characteristic dimensions of the surface corrugation with a rectangular profile. The effects of the characteristic properties of an ultrasound beam such as beam diameter, temporal pulse width of the beam, central frequency of the beam, on the possibility and accuracy of geometrical characterization are theoretical discussed. The experimental illustrations of the theoretical conclusions are obtained by the C-scan imaging of three corrugated brass samples.

The investigation of the interaction of ultrasound with composite structures is mainly focused on the characterization of impact defects of composite plates. The case in which the received signal is corrupted by high-level unavoidable noise caused by the data acquisition system is investigated and presented in Chapter VI. Spectral analysis of the windowed signal is proposed to process the noise-corrupted signals and to extract effective data property for defect characterization. The C-scan images obtained form spectral data processing are compared with those obtained from temporal data processing. It shows that the spectral data processing method can give better images than the temporal data processing method, and it also promises the possibility to accurately characterize the dimension of inner defects.

Chapter VIII presents the investigation in comparing different techniques of immersion ultrasonic testing of the impact defect in composite plates. The purpose of this work is to find the optimized method to characterize the designed impacted defect in the carbon/epoxy composite plates. Both testing configurations and signal processing methods are compared in terms of their reliability and efficiency.

All the work presented in this thesis is summarized in Chapter VIII, the last chapter of this thesis. The future work in both categories, interaction of ultrasound with periodic structures and characterization of impact defects of composite plates, is also presented in this chapter.

## RESUME DU CHAPTRE II

Dans le spectre d’un faisceau acoustique à large bande réfléchi par une surface périodiquement ondulée, des anomalies spectrales telles que des creux pointus ont été précédemment observées et identifiées comme des anomalies acoustique de Wood, analogues à un phénomène similaire observé en optique. Dans ce travail, une étude approfondie sur l’origine physique de anomalies acoustique de Wood est faite. L’étude expérimentale est réalisée sur une surface de laiton périodiquement ondulée avec un profil rectangulaire. Les explications existantes de Wood anomalie acoustique sont examinées et évaluées sur la base de l’analyse des résultats expérimentaux obtenus à partir de trois types d’interfaces: liquide-solide, solide-liquide et solide-air. Une pointe spectrale est signalée pour la première fois dans ce travail comme un nouveau type d’anomalie dans le spectre de réflexion. l’Analyse du domaine temps-fréquence est introduite dans l’analyse anomalie acoustique de Wood et le sonogramme résultant de la réflexion spéculaire réfute la perte d’énergie hypothèse communément admise sur l’origine des anomalie acoustique de Wood. Il est également signalé pour la première fois que l’inclinaison spectrale n’est pas une interférence destructive réelle, mais un monde virtuel provoqué par le procédé de traitement de données (FFT) . Sur la base de la différence de phase entre les signaux réfléchis, un minimum spectral s’avère être le résultat d’un effet d’annulation de phase, tandis qu’une pointe spectrale est le résultat d’ un effet de phase renforce. Enfin, une description complète du processus physique de anomalie de Wood est proposée.

## CHAPTER II  ACOUSTIC WOOD ANOMALY PHENOMENON

### 2.1 Introduction

The interaction of acoustic waves with periodically corrugated surfaces as occurring in many practical situations has been intensively studied both theoretically [1-16] and experimentally [17-19]. One very peculiar research topic in this field is a phenomenon observed in the spectrum of specular reflection. When a broadband acoustic beam is normally incident onto a periodically corrugated surface, the incident bulk wave will be diffracted by the surface corrugation and the diffracted waves consist of the specularly reflected wave (zero order diffraction) and higher order diffracted waves. When examining the spectrum of the specular reflection, sharp dips have been observed. This kind of spectral anomaly is similar to the dark band first observed by Wood [20] in the reflection spectrum of light from a diffraction grating, and, therefore, has been historically identified as acoustic Wood anomaly.

The first attempt to explain the origin of the optical spectral anomaly, i.e. the commonly known Wood anomaly, was made by Lord Rayleigh [21] and he pointed out that a spectral anomaly is expected at a particular wavelength of light if the higher order of that wavelength is just passing out of the grating, i.e. is emerging tangentially to the grating surface. A very short time later, Rayleigh revisited this phenomenon in his well-known dynamic theory of grating [22] trying to develop his idea about optical Wood anomaly, but arriving at no more satisfactory explanation.

The correlation between a spectral anomaly and a diffraction order generated along the grating surface in Rayleigh’s explanation of optical Wood anomaly was later applied to the explanation of acoustic Wood anomaly, and it is further stated as that a spectral
anomaly appears at the transition of a diffracted order from being a propagating mode to being an evanescent mode or vice versa [23-26]. This condition for the occurrence of spectral anomaly is actually a special case of the cutoff condition for normal incidence according to the classical grating equation [17]. Furthermore, the evanescent wave mode, which is possibly generated along the periodically corrugated interface, is assumed to be surface acoustic wave [23, 25-27]. Thus, the so-called mode conversion assumption is reached, which can be summarized as that a spectral anomaly in the reflection spectrum occurs at a frequency at which the incident bulk wave (a propagating mode) is converted to a surface acoustic wave (an evanescent mode) on the periodically corrugated interface through diffraction. And this assumption of mode conversion has been widely applied in the interpretation of acoustic Wood anomaly obtained in both experimental observations [23-26] and numerical simulations [24-27].

The identification of the type of the surface acoustic wave on the corrugated surface predicted by the mode conversion assumption is through a velocity matching method. In this method the wave velocity of the evanescent wave possibly generated on the corrugated surface is compared with the velocities of all the known waves, and the type of the wave whose velocity is the closest to that of the evanescent wave is then identified as the type of the mode converted evanescent wave [23, 25-27]. With respect to the experimentally observed mode type into which the incident bulk wave is converted, on liquid-solid interfaces Rayleigh mode and longitudinal wave mode have been first identified and studied [23], and Scholte mode was identified later [25]. Experimental observations also revealed that Rayleigh mode [23, 26] and Stoneley mode [26] exist on corrugated solid-liquid interfaces, and that only Rayleigh mode [23, 24] exists on corrugated solid-air interfaces.

The possibility of wave mode conversion caused by interface corrugation promises
its application in signal processing by using a diffraction grating as a device to realize the transformation from bulk waves to surface acoustic wave for non-piezoelectric materials [29, 30]. The study of the physical origin of acoustic Wood anomaly also suggests some potential applications such as nondestructive testing (NDT) for characterizing interfaces and quality of bonding of layered materials [23].

Although the mode conversion assumption is able to identify the converted modes at anomaly frequencies for many cases, it fails for some case [24]. Furthermore, up to now there has been no profound theory supported by solid experimental results, for the actual physical mechanism of mode conversion on corrugated surfaces, and for the direct cause of Wood anomalies. There exist some explanations or assumptions for acoustic Wood anomaly, but their limitations only permit indications of what possibly happens in a specific aspect of the problem without giving a big picture.

The main purpose of this work is to thoroughly examine the existing explanations and assumptions concerning the physical origin of the acoustic Wood anomaly, and then to reach a complete understanding of this phenomenon. All the investigations in this study are based on the analysis of the reflection from a periodically corrugated brass surface. In most previous theoretical and experimental studies the corrugation profiles that have been investigated are triangular (sawtooth) profile [23, 25-27], trapezoidal profile ${ }^{26}$ and sinusoidal profile [26, 27], while the profile investigated in this work is a rectangular profile, which has been used before to investigate the physical phenomenon of backward beam displacement [31, 32]. In addition, all the three common interfaces, liquid-solid, solid-liquid and solid-air (stress free) interfaces, are investigated in this study hence providing a complete and conclusive investigation.

### 3.2 Samples and Experimental Setup

The sample investigated in this study is a brass block with a periodically corrugated
surface on one side and a smooth surface on the other side. The corrugated surface has a rectangular profile with a corrugation periodicity of $185 \mu \mathrm{~m}$ and a corrugation height of $25 \mu \mathrm{~m}$.

In order to assure the repeatability and consistency of the experimental results, four pairs of broadband immersion transducers, ‘Valpey Fisher’ transducers of 5 MHz and 10 MHz, and ‘NDT Systems’ transducers of 15 MHz and 20 MHz, are applied in this study. The experimental results of the investigated spectral anomaly obtained using different transducers, each in their own spectrum coverage, are consistent with each other. Because the main features of spectral anomalies for the sample investigated here appear in the vicinity of 10 MHz, the results obtained using the 10 MHz transducers are shown in this paper for illustration and discussion.

The pulse-echo technique is applied in this study to obtain the reflections from the periodically corrugated water-brass interface as shown in Figure 2-1 (a) and from the corrugated brass-water and brass-air interfaces as shown in Figure 2-1 (b). In order to illustrate the effect caused by corrugated interfaces on reflected sound, the reflections from flat water-brass, brass-water and brass-air interfaces have been collected using the same experimental configuration and have consequently been compared with those obtained from their respective corrugated interfaces. In addition, a polar scan over a range of 12° to 112° with respect to the normal direction to the corrugated interface was performed for the case where a beam is perpendicularly incident on the corrugated water-brass interface. The purpose of this polar scan is to check if there is a propagating wave being generated on and propagating along the water-brass interface, or being generated and reradiated back to the incident medium (water), and accordingly evaluate the reliability of the assumption that the observed spectral dip is due to energy loss caused by the generated propagating wave.

All the experiments have been performed by means of a customer-designed scanner manufactured by ‘Inspection Technology Europe BV’. This scanner has an angular resolution of 0.01° which ensures the ability to orient incident beams perfectly perpendicular to the corrugated interface. The experimental data were acquired using ‘Winspect’ data acquisition software and were further processed using Matlab. And data analysis has been performed in time domain, frequency domain and time-frequency domain as demonstrated in the next section.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-028_1229_1453_1003_303.jpg)

Figure 2-1 Schematics of the experimental setup for obtaining reflections from periodically corrugated rectangular (a) water-brass interface and (b) brass-water and brass-air interfaces, and the setup of (c) polar scan of the diffraction field.

In order to make accurate analysis of the experimental observations, especially to
check the reliability of the existing assumptions about the physical origin of spectral anomalies, the reference wave velocities of different wave types used in this work have been experimentally measured under the same conditions as the above investigation. All the reference velocities that should possibly be considered in the mode conversion assumption are listed in Table 2-1. The longitudinal wave velocity in water $\left(c_{f}\right)$ was measured in a pitch-catch ultrasonic mode; the longitudinal wave velocity $\left(c_{l}\right)$ and the shear wave velocity $\left(c_{s}\right)$ of brass were measured in both contact and immersion ultrasonic pitch-catch mode. The Rayleigh velocity $\left(c_{R}\right)$ of brass was obtained from its generation condition on a flat water-brass interface represented by the following equation [33].

$$
c_{R}=\frac{c}{\sin \theta_{R}}
$$

in which the Rayleigh angle $\left(\theta_{R}\right)$ of brass was measured on the smooth side of the brass sample using the same polar scan system according to the phenomenon of reflection beam split.

Table 2-1 Related wave velocities
| $c(\mathrm{~m} / \mathrm{s})$ | $c_{l}(\mathrm{~m} / \mathrm{s})$ | $c_{s}(\mathrm{~m} / \mathrm{s})$ | $c_{R}(\mathrm{~m} / \mathrm{s})$ |
| :— | :— | :— | :— |
| 1480 | 4259 | 2341 | 2051 |

### 2.3 Results and Discussion

In this section the experimental observation of spectral anomalies will be presented first. Next is a review of the existing explanations of the acoustic Wood anomaly together with the examination and evaluation of these explanations and assumptions based on the experimental results obtained in this study. Then, a new explanation, which is supported by experimental results, will be given showing a relatively complete picture
of the physical mechanism of the acoustic Wood anomaly. Finally the experimental results for brass-water and brass-air interfaces will be shown.

### 2.3.1 Observation of Spectral Anomalies

The spectra of the reflections from flat and periodically corrugated water-brass interfaces are compared in Figure 2-2 (a). The amplitude difference and the ratio of these two spectra are shown in Figure 2-2 (b) and (c) respectively. Normally in the literature the effect of the corrugated interface on the reflection is illustrated by the amplitude ratio of different frequency components, between flat and corrugated interface reflections as shown in Figure 2-2 (c). The reason why the amplitude difference (Figure 2-2 (b)) is shown in this study is to illustrate the energy change caused by diffraction for different frequencies.

From the three subfigures of Figure 2-2 a sharp spectral dip is observed at 8.23 MHz, and this observation confirms the observation made in the literature concerning the acoustic Wood anomaly. It should be noted that except for the sharp spectral dip at 8.23 MHz, there is a spectral tip appearing at 10.89 MHz although it is not as visible as the spectral dip. This kind of spectral anomaly has not been reported in the literature concerning the observation of spectral anomalies from reflection spectrum, but in Wood’s original paper [20] such an enhanced reflection in optics appearing as a bright band in the spectrum was reported. A possible reason why such a spectral tip has not been reported in earlier experimental work is that spectral tips cannot be easily generated by the corrugated structures other than rectangular ones because the earlier experiments are usually performed on either a triangular (sawtooth) profile or a sinusoidal profile. Another possible reason is that such a spectral peak anomaly is hardly noticeable in the spectrum when represented as the ratio of the reflection spectra from a corrugated
surface and a flat one as done by the researchers who reported on this topic in the past decades. The observation that the spectral tip at 10.89 MHz is less visible in Figure 2-2 (c) than in Figure 2-2 (a) and (b) suggests that the signal representation method certainly plays a role in the visibility of anomalies. Moreover, the improvement in experimental equipment may also be a reason for the fact that such an enhanced anomaly is observed in this work, but not in previous work. In addition, the existence of such a spectral tip will be confirmed by Figure 2-4 (c) and Figure 2-5 (d).

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-031_1280_1270_1025_395.jpg)

Figure 2-2 Comparison of the reflection spectra from flat and periodically corrugated water-brass interfaces: (a) shows the respective spectra of flat surface reflection and corrugated surface reflection; (b) is the amplitude difference between of the two spectra; and (c) is the ratio of amplitudes of the two spectra.

### 2.3.2 Existing Explanations of Acoustic Wood Anomaly

The key problem concerning the phenomenon of acoustic Wood anomaly is its physical origin. In order to fully understand the physical origin of this phenomenon two questions should be answered: (i) at which frequency is the spectral anomaly expected? and (ii) what happens at the anomaly frequency? The first question is about the determination of the anomaly frequency; the second one is about the physical mechanism of the spectral anomaly. The most widely accepted theoretical explanation for the first question is the so-called mode conversion assumption, while no such commonly accepted explanation exists for the second question. In the following subsections we will first review the existing explanations for the two questions and then put them to the test by the experimental results obtained in this study.

### 2.3.2.1 On Mode Conversion Assumption

The main idea of the mode conversion assumption originates from Rayleigh’s finding for optical Wood anomaly [21] that a spectral anomaly is expected at a particular wavelength (frequency) of light whose higher order diffraction is generated along the grating surface. In acoustics this condition has been developed to be that a spectral anomaly in the reflection spectrum from a periodically corrugated interface is expected to appear at the frequency at which a diffracted order converts from a propagating mode to an evanescent mode on the interface, or vice versa. For normal incidence the propagating mode refers to the incident bulk wave, while the evanescent mode is further assumed to be surface acoustic wave that can possibly be generated by the surface corrugation through diffraction.

The specific condition for the mode conversion from an incident bulk wave to a different order on the corrugated surface can be derived from the classical grating equation:

$$
\frac{\sin \theta^{i}}{\lambda^{i}}+\frac{\sin \theta_{m}^{d}}{\lambda^{d}}=\frac{m}{\Lambda}
$$

with $\theta^{i}$ the incident angle of a beam, $\theta^{d}{ }_{m}$ the diffraction angle of the $\mathrm{m}^{\text {th }}$ order, $m=0$, $\pm 1, \pm 2 \ldots, \lambda^{i}$ is the wavelength of the incident wave, $\lambda^{d}$ is the wavelength of the diffracted wave, $\Lambda$ is the periodicity of the surface corrugation. In this study we consider the case in which a bulk wave is normally incident upon the corrugated surface, i.e., $\theta^{i}=0^{\circ}$, or $\sin \theta^{i}=0$. Accordingly, the direction of diffraction of different orders can be expressed by the simplified classical grating equation:

$$
\sin \theta_{m}^{d}=m \frac{\lambda^{d}}{\Lambda}
$$

When a diffraction order is generated along the interface, i.e., $\theta_{m}^{d}=90^{\circ}$, or $\sin \theta_{m}^{d}=1$, a transition from a propagating mode to an evanescent mode, or vice versa, occurs. Under this condition the classical grating equation for normal incidence can be further simplified as

$$
m \frac{\lambda^{d}}{\Lambda}=1
$$

By applying the relationship between wave velocity $c$, frequency $f$ and wavelength $\lambda$, i.e., $c=f \lambda$, the velocity of the diffracted wave can be obtained as

$$
c^{d}=\frac{f \Lambda}{m}
$$

Based on the analysis above, the type of the surface acoustic wave possibly converted from the incident bulk wave can be determined through velocity matching as illustrated in the following two steps.

Step I: By substituting the wave frequency ( $f$ ) with the anomaly frequency obtained from the reflection spectrum and choosing a proper number for the diffraction order $(m)$, a possible velocity of diffracted wave $\left(c^{d}\right)$ can be determined from Equation (2-5).

Step II: Compare the value of $c^{d}$ with the velocities of all the known waves existing in both media such as the longitudinal wave and shear wave, or existing at the interface (surface acoustic waves) such as Rayleigh wave and Scholte-Stoneley wave, to find the wave mode whose velocity is closest to $c^{d}$, and then identify this wave as the one converted from the incident bulk. The cases of mode conversion experimentally observed in the literatures are summarized in Table 2-2 in which the type of corrugated interface, the type of corrugation profile, the relationship of the wave velocities possibly involved, and the converted mode are all listed. It should be noted that the converted mode identified by matching the sound velocity in water has been given different names in the literature such as longitudinal mode [23] and Scholte mode [25] for liquid-solid interface and the Stoneley mode [26, 27] for solid-liquid interface.

Table 2-2 Summery of experimentally observed mode conversion at anomaly frequencies for different corrugated interfaces, profile, and velocity relationship. Here $c_{\boldsymbol{f}}$ is the longitudinal wave velocity of fluid, $c_{R}$ the Rayleigh wave velocity, $c_{l}$ the longitudinal wave velocity, and $\boldsymbol{c}_{\boldsymbol{s}}$ the shear wave velocity of solid.
| Interface | Profile | Velocities | Converted mode |
| :— | :— | :— | :— |
| Liquid-solid | Triangular | $c_{f}<c_{R}<c_{s}<c_{l}$ | Longitudinal, Scholte, Rayleigh |
| Liquid-solid | Triangular | $c_{R}<c_{s}<c_{f}<c_{l}$ | Rayleigh, Longitudinal |
| Solid-liquid | Triangular | $c_{f}<c_{R}<c_{s}<c_{l}$ | Rayleigh |
| Solid-liquid | Trapezoidal | $c_{f}<c_{R}<c_{s}<c_{l}$ | Stoneley, Rayleigh |
| Solid-air | Triangular | $C_{R}<C_{s}<C_{l}$ | Rayleigh |

In this study two spectral anomalies have been identified for the corrugated waterbrass interface: a spectral dip at 8.23 MHz and a spectral tip at 10.89 MHz. According to Equation (2-5) these two frequencies correspond to a velocity value of 1523 m/s and 2015 m/s respectively if only the first diffraction order $(\mathrm{m}=1)$ is being considered; these velocities are listed as velocity estimations in Table 2-3. According to the velocity matching method introduced in the mode conversion assumption the closest wave velocities to the above velocity estimates are the longitudinal velocity in water (1480 m/s) and the Rayleigh velocity of brass (2051 m/s) respectively. Therefore, the anomaly at 8.23 MHz is identified as the one caused by the conversion of the incident longitudinal waves in water from a propagating mode normally towards the interface to an evanescent mode along the interface, while the anomaly at 10.89 MHz by the conversion of the incident longitudinal wave to a Rayleigh-type surface wave. The precision of the velocity matching for both anomalies is 2.9% and -1.8% respectively. All the results and related data considered in the above identification process are listed in Table 2-3. In summary, with such high precisions the mode conversion assumption seems to be able to answer the question about the determination of anomaly frequencies, but say little about the physical mechanism of Wood anomaly.

Table 2-3 Identification of converted modes at anomaly frequencies for the corrugated water-brass interface based on mode conversion theory.
| Type of anomaly | Spectral dip | Spectral tip |
| :— | :— | :— |
| Anomaly frequency (MHz) | 8.23 | 10.89 |
| Velocity estimate (m/s) | 1523 | 2015 |
| Closest velocity measured (m/s) | 1480 | 2051 |
| Velocity difference (%) | 2.9 | -1.8 |
| Type of mode converted | Longitudinal | Rayleigh |

### 2.3.2.2 On the Assumption of Energy Loss

This assumption aims to answer the second questions above concerning the physical mechanism of the spectral anomaly. Because only spectral dips had been observed when this assumption was proposed, it therefore only attempted to explain the cause of spectral dips. In this assumption spectral dips are interpreted as the consequence of energy loss from the specular reflection due to some kind of physical mechanism [28]. It is possible that a propagating surface wave is generated, and its propagation along the interface carries the missing energy away [28]. It is also possible that the energy at the anomaly frequency is diffracted to other angular positions [23]. If Rayleigh wave is generated on the surface the energy loss can be caused by reradiating the energy back to the incident medium due to the leaky nature of Rayleigh waves [27].

In order to evaluate the reliability of the energy loss assumption a polar scan of the diffraction field of the water-brass interface over a range of 100° is performed. The resulting time domain representation (angular B-scan) and frequency domain representation (angular spectrogram) are shown in Figure 2-3 (a) and (b) respectively.

If a propagating surface wave is generated and it carries away the energy at the anomaly frequency (8.23 MHz in this study) from the specular reflection, a significant amount of energy at 8.23 MHz is expected to appear at around 90° in the diffraction field. However, Figure 2-3 shows that there is no such an energy enhancement appearing at that angular position in both time domain and frequency domain. Figure 2-3 also shows that most energy of the diffraction field is confined in the angular region smaller than 90° and almost no energy can be observed beyond 90°. These observations strongly weaken the argument of the generation of a propagating surface wave.

If the wave energy at the anomaly frequency is diffracted to other angular positions, or reradiated back into the incident medium, a visible energy increase at 8.23 MHz
should be observed in the diffraction field. There is indeed an increase of energy appears at about 8.23 MHz for almost all the angles below 70° according to the angular spectrogram shown in Figure 2-3 (b), but there is also a energy decrease by its side at about 8.4 MHz over the same angular range. Thus, it is not proper to claim that the energy enhancement observed at about 8.23 MHz in the diffraction field is the energy missing from specular reflection.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-037_1535_1292_880_392.jpg)

Figure 2-3 (a) B-scan and (b) angular spectrogram of diffraction field obtained from the periodically corrugated water-brass interface for normal incidence.

To summarize, all these observations do not suggest that the energy loss assumption is capable of explaining the physical origin of sharp spectral anomalies. In addition, another distinct shortcoming of this assumption is that it only attempts to explain the origin of spectral dips not considering the origin of spectral tips at all.

Since the assumption of energy loss cannot explain the physical mechanism of spectral dips, it is better to re-examine the Wood anomaly phenomenon from the very foundations by analyzing the specular reflection field in which this phenomenon appears. The waveforms of the reflections from both flat and corrugated water-brass surfaces are compared in Figure 2-4 (a). It can be observed that before $119.65 \mu \mathrm{~s}$ both reflections have a similar wave pattern although with different amplitudes, but after $119.65 \mu \mathrm{~s}$ their wave patterns are totally different: the flat surface reflection is relatively flat, while the corrugated surface reflection contains a series of oscillations. The time domain difference between the reflections from flat and corrugated interfaces observed in Figure 2-4 (a) together with their difference in the frequency domain observed in Figure 2-4 actually inspired us to investigate this phenomenon from a new perspective, i.e. through analysis in the time-frequency domain ${ }^{34}$.

The time-frequency domain representation (sonogram) of the flat surface reflection and the corrugated surface reflection are shown in Figure 2-4 (b) and (c) respectively. One observation obtained from the comparison of the two sonograms is that the big bangs of both reflections have a similar time-frequency domain shape with different amplitudes (represented by color intensity) and this confirms the time domain comparison of their waveforms before $119.65 \mu \mathrm{~s}$, which shows both reflections have a similar wave pattern but different amplitudes. The distinct difference between these two sonograms is that the reflection from the corrugated surface has two long tails whose central frequencies are 8.23 MHz and 10.89 MHz, respectively. This suggests that the
oscillations in the

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-039_1347_1419_433_332.jpg)

Figure 2-4 Comparison of the reflections from flat and periodically corrugated water-brass interfaces in time domain and time-frequency domain: (a) shows the waveforms of the two reflections; (b) is the sonogram of the flat interface reflection; and (c) is the sonogram of the corrugated interface reflection.

waveform after $119.65 \mu \mathrm{~s}$ of the corrugated interface reflection contains two frequency components that exactly correspond to the frequencies of the observed Wood anomalies. Such an observation suggests that the frequency components at anomaly frequencies are not missing from specular reflections, but only retarded in time and reach the receiving transducer at a later time. Moreover, the fact that the energy at the anomaly frequency of
8.23 MHz is not missing, but still contained in the specular reflection suggests that the energy enhancement observed in Figure 4-3 (b) probably has nothing to do with the occurrence of the spectral dip in the reflection spectrum. In summary, the time-frequency analysis suggests that the occurrence of acoustic Wood anomalies is not caused by energy loss from specular reflection, and therefore further falsify the argument that energy loss is the cause of the spectral dips.

### 2.3.2.3 On the Assumption of Finite Beam Effect

This assumption is also an attempt to explain the physical mechanism of spectral dips, not spectral tips. It has been shown theoretically and experimentally that an incident beam with a finite width can be widened or even splitted into two beams in the reflection from a periodically corrugated interface and this phenomenon is called finite beam effect [35]. Because bounded beams with finite widths were used in all the experiments from which the spectral anomalies were observed, some researchers claimed that the finite beam effect causes the spectral dips in the reflection spectrum from a periodic surface [36]. For normal incidence in the pulse-echo configuration the emitter and the receiver are the same transducer, thus the widened reflection beam will result in that part of the incident energy cannot be reflected back to the receiving transducer, and this partial energy loss causes the observed anomaly [28]. Although it has been proved that the depth of a spectral minimum does relate to the incident beam width [36], some researchers showed that it requires an incident beam whose width is far smaller than the beam used in the experiments to produce a spectral dip with the same depth as the one identified as a Wood anomaly [24]. Therefore, this assumption is not efficient for explaining the physical origin the Wood anomaly.

### 2.3.2.4 On the Assumption of Surface Resonance Generation

Generation of oscillations at the corrugated surface is another assumption for the physical mechanism of Wood anomaly. Numerical simulation of the particle displacement of a corrugated surface based on the boundary integral equation method ${ }^{10}$ revealed a noticeable surface resonance at the frequencies corresponding to the transition of a diffraction order from propagating mode to evanescent mode[24]. Experimentally it has been shown that the tailing wave, which follows the main bang (direct reflection) in a waveform of reflection from a corrugated surface, has the same frequency as the frequency at which an anomaly occurs in the reflection spectrum [24]. This observation has of course triggered the interpretation that a Wood anomaly is caused by a resonance of the corrugation resulting from the mode conversion of an incident bulk wave into surface motion. In this framework it is generally believed that as these resonant waves are reradiated back to the receiving transducer, they destructively interfere with the direct specular reflection from the corrugation and thus cause a sharp spectral anomaly. It has been pointed out that the spectral component at the anomaly frequency of the direct reflection is likely to be opposite in phase with that of the oscillations [24, 32], but no proof has been given.

Similar to the two assumptions discussed above this assumption also only deals with spectral dips. In order to make such spectral dips possible three conditions have to be satisfied under this assumption: (i) generation of surface resonance, (ii) normal radiation of the resonance energy back to the receiver and (iii) opposite phase between the resonant waves and the component of direct reflection at the anomaly frequency. The current study will check these three conditions experimentally.

First, tailing oscillations have been experimentally observed from the specular reflection in the current experiments. In order to better illustrate these oscillations, the main bang and the tail of the normally reflected signal from the brass-water interface are represented separately both in time domain and in frequency domain and the results are shown in Figure 2-5. It can be seen that the waveform (Figure 2-5 (a)) and the spectrum (Figure 2-5 (b)) of the main bang of the reflected signal are similar to those of a flat surface reflection (Figure 2-4 (a) and Figure 2-2 (a)), whereas the tail is totally different. A series of oscillations can be observed in the waveform of the tail as shown in Figure 2-5 (c) and the main frequency components of the these oscillations, as shown in Figure 2-5 (d), are exactly the anomaly frequencies observed in this study, namely 8.23 MHz and 10.89 MHz. Because these oscillations, or ringing patterns, originate from the corrugated surface, it can be concluded that some type of surface resonance is generated at the anomaly frequencies.

Second, the fact that the surface oscillations coming from the corrugated surface have been detected by the receiving transducer, which is located at the normal position of the interface, suggests that the condition of normal radiation of resonance energy is satisfied. But it is not clear in this assumption why the resonance energy can be normally radiated back to the receiver. In fact, a close examination of the diffraction field shown in Figure 2-3, reveals that similar tailing oscillations as shown in Figure 2-5 (c) appear beyond 12°. This means it is possible that the radiation of the oscillation energy is spreading to a larger angular range, rather than being confined to the normal position, and this aspect will be discussed in the next section.

Important here is the fact that in the overall spectrum shown in Figure 2-2 the anomalies appear as a spectral dip at 8.23 MHz and a spectral tip at 10.89 MHz, while in the separate spectral analysis shown in Figure 2-5 (c) both anomalies exist in the form of
spectral tips. This suggests that the apparent appearance of a Wood anomaly is affected not only by windowing the signal in the time domain, but also by the method used in the data processing, i.e., Fast Fourier Transform (FFT). This fact has never been pointed out in earlier reported work.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-043_1751_1342_760_361.jpg)

Figure 2-5 Comparison of the main bang and the tail of the reflection from corrugated

water-brass interface: (a) waveform and (b) amplitude spectrum of the main bang; (c) waveform and (d) amplitude spectrum of the tail.

In the time domain, if for any reason only the main bang of the reflected signal is windowed and spectrally analyzed, no anomaly will be observed as shown in Figure 2-5 (b). Only when the window is long enough to cover not only the main bang but also the oscillating tail of the signal, the Wood anomaly can be observed.

The FFT is a widely used analysis technique and the earlier research work on Wood anomalies is highly determined by this technique. Even though it is a thorough, stable, reversible and easy-to-apply numerical technique based on the consistent and well established theory of Fourier analysis, one must not forget the essence of this theory, namely that it is an overall analysis. A spectrum obtained by FFT is hence an overall representation of all the frequency components contained in the windowed signal, and it does not directly indicate the temporal distribution of each of these frequency components. For this reason it is actually impossible to conclude if the energy at the spectral dip is really physically missing or rather is a phantom due to the analysis technique. To gain insight it is helpful to study a sonogram of the obtained reflection signal instead. In such time-frequency domain representation the temporal distribution of each frequency component is shown and therefore makes it possible to determine if certain frequencies are really missing or not.

Another point necessary to make clear about FFT is that its representation of the amplitude of each individual frequency component is not a simple magnitude summation of the amplitudes of all the components at that frequency contained in the analyzed signal, but a complex accumulation taking into account the phase of each component. If for instance two components of the same frequency have a phase difference larger than 90°, their cumulative representation will show a cancelling effect; this phenomenon of
course becomes extreme when the components are 180° out of phase and total cancellation appears. Similarly, if two components of the same frequency have a phase difference smaller than 90°, there will be an enhancing effect when cumulated with the maximum accumulation effect appearing when they are perfectly in phase. Because the phase relationship of two components with the same frequency determines their accumulating result, the above two cases can be called a phase cancelling effect and a phase enhancing effect respectively.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-045_933_1287_1015_382.jpg)

Figure 2-6 Comparison of the phase spectra of the reflection from (a) flat and (b) corrugated water-brass interfaces.

In the current study the spectral dip at 8.23 MHz is actually the result of a phase cancellation between the components of this frequency in the main bang and the oscillating tail of the corrugated surface reflection; while the spectral tip at 10.89 MHz is the result of a phase enhancement between the respective frequency components in the main bang and the tail. These conclusions can be supported by comparing the phase
spectrum of the signal reflected from the flat surface with that from a corrugated surface, as shown in Figure 2-6. It can be observed that there is no phase shift in the phase spectrum coming from the flat surface shown in Figure 2-6 (a), while there is a distinct phase shift appearing at about 8.23 MHz in the phase spectrum coming from the corrugated surface. This phase shift supports the argument that the spectral dip at 8.23 MHz results from a phase cancelling effect. Additionally, the fact that no phase shift is observed at 10.89 MHz is the proof for the occurrence of a phase enhancing effect at this frequency.

At last, it should be pointed out that the researchers who recognized the generation of surface resonance claimed that the sharp spectral dips are caused by the destructive interference between the surface resonance travelling back to the transducer and the specular reflection [24]. Strictly speaking this claim is not true because the specular reflection (main bang) and the surface resonance (oscillating tail of the corrugated surface reflection) do not interact with each other either in the space domain or in the time domain. The spectral dip is therefore not an actual destructive interference, but a virtual ‘ghost’ caused by the FFT data processing method.

### 2.3.2.5 On the Assumption of Double Mode Conversion

This assumption states that mode conversion caused by the corrugated interface occurs twice. In the first mode conversion the normally incident bulk wave is converted into a surface mode, and this converted surface mode is attenuated during its propagation along the interface while it is being converted back to a propagating bulk mode. This propagating wave converted in the second mode conversion reaches the receiving transducer as part of the entire signal that is captured as the reflected signal. It is clear that the direction of the incident wave that undergoes the second mode conversion is
parallel to the interface, i.e., $\theta^{i, I I}=90^{\circ}$, or $\sin \theta^{i, I I}=1$ with the second superscript $I I$ standing for the second mode conversion process. The classical grating equation for this case can be written as

$$
\frac{1}{\lambda^{i, I I}}+\frac{\sin \theta_{m}^{d, I I}}{\lambda^{d, I I}}=\frac{m}{\Lambda}
$$

Considering that the incident wave in the second mode conversion is actually the mode converted surface wave in the first mode conversion, i.e., $\lambda^{i, I I}=\lambda^{d, I}$, and that the mode converted wave in the second mode conversion has the same wave type as the incident wave in the first mode conversion, i.e., $\lambda^{d, I I}=\lambda^{i, I}$, the direction of the twice mode converted bulk wave can be obtained from Equation (2-4) and Equation (2-6) as

$$
\sin \theta_{m}^{d, I I}=\lambda^{i, I}\left(\frac{m}{\Lambda}-\frac{1}{\lambda^{d, I}}\right)=0
$$

or $\theta^{d, I I}=0^{\circ}$. Hence, the incident bulk wave is converted back again to a bulk mode traveling vertically back to the receiving transducer. Due to the fact that this twice mode converted bulk wave has a time delay (phase difference) with respect to the directly reflected bulk wave, it is assumed that they destructively interfere with each other, resulting in the so-called acoustic Wood anomaly in the reflection spectrum.

As discussed in previous section the assumption of surface resonance generation only claims that the generated surface oscillations are reradiated back to the receiver, but does not explain why they behave so. However, the assumption of double mode conversion clearly shows that the direction of the re-radiated energy from the corrugated surface is perpendicular to the interface. This perfectly explains why the receiver, which is located in the normal position of the interface, can receive the surface oscillations.

Now the question is if the oscillating energy only propagates in the normal direction
and finally reaches the receiver, not going to any other directions; in other words, if the diffraction of these surface oscillations governed by the classical grating equation is the only physical process occurring to these oscillations on the surface. In order to check this we need to have a close look at the diffraction field in Figure 2-3 in both time domain and frequency domain. As shown in Figure 2-4 (c) and Figure 2-5 the oscillating tail of the received signal has different spectral distribution from that of the main bang (direct reflection) and Figure 2-3 (a) shows that the diffraction signal at each angular position has a similar oscillating tail as the specular reflection. These two observations inspired us to analyze the trailing signals of diffraction. For the convenience of illustration the trailing oscillations of the diffraction from 12° to 30° are chosen and their time domain and frequency domain representations are shown in Figure 2-7 (a) and (b). A distinct feature of the angular spectrogram of the oscillating tails shown in Figure 2-7 (b) is a straight angle-frequency fringe appearing at about 8.23 MHz, the frequency of the spectral dip observed in this study. This confirms the observation from Figure 2-3 (b) that there is an energy enhancement existing at 8.23 MHz, which originates from the surface resonance of longitudinal mode. In other words, the surface oscillations of longitudinal mode radiate their energy to the whole diffraction field not limiting to the normal position as predicted by the assumption of double mode conversion. Thus, this assumption cannot fully explain the propagation of surface resonance of longitudinal mode. Because there is no similar angle-frequency feature as the one at 8.23 MHz for the surface resonance of Rayleigh mode, it can be assumed that this assumption can properly explain the radiation behavior of Rayleigh mode surface oscillations.

It should be pointed out that the angle-frequency fringe locating between 10 MHz and 15 MHz, which can also be observed from Figure 2-7 (b), has been theoretically proved to be the diffraction of a longitudinal mode coupling on the surface. Because this
physical mechanism is not related to the topic of this work, it will not be elaborated here.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-049_789_1429_414_310.jpg)

Figure 2-7 (a) B-scan and (b) angular spectrogram of the oscillating tails of diffraction obtained from the periodically corrugated water-brass interface for normal incidence.

### 2.3.3 New Explanations of Acoustic Wood Anomaly

After reviewing the existing assumptions and explanation of the acoustic Wood anomaly and evaluating them based on the analysis of the experimental results obtained in this study, a relatively complete understanding of this phenomenon is presented in this section. Summarizing all the investigations, including the current one, on the physical origin of the so-called acoustic Wood anomaly, the physical process from a beam normally incident onto a periodically corrugated interface to the spectral anomalies appearing in the spectrum of the specular reflection from that interface can be described as followed:

1. Conversion of a normally incident broadband bulk wave to a surface-type mode at the transition frequency. This is the first mode conversion process that occurs at the corrugated interface. In this process a bulk wave propagating in the

incident medium is converted to an evanescent surface wave mode on the interface through diffraction governed by the classical grating equation. Not all the frequency components of the incident broadband wave are mode converted in this process, but only those corresponding to the generation of an order of diffraction along the interface. Thus, the mode converted surface acoustic wave mode has a single frequency, which is the transition frequency from a propagating wave to a specific type of surface acoustic wave. The converted surface acoustic wave modes that have been experimentally identified are the Rayleigh mode for all three types of periodic interfaces (liquid-solid, solid-liquid and solid-air interfaces), and the longitudinal mode, which is also called Scholte mode or Stoneley mode by some researchers, for periodic liquid-solid and solid-liquid interface.
(ii) Generation of surface oscillations. The mode-converted surface-type wave does not propagate at the corrugated interface as it does along a flat interface, but is strongly attenuated by the surface corrugation. The attenuated surface mode is coupled with the corrugated surface in the form of surface oscillations.
(iii) Conversion of the mode-converted surface-type mode back to a bulk mode. This is the second mode conversion process occurring at the corrugated interface. In this process the energy of the surface oscillations is radiated back into the incident medium. If considering the mode-converted surface-type wave mode as incident wave, the classical grating equation can perfectly explain why the receiver, which is located at the normal position of the interface, can receive the surface oscillations of any mode such as the surface oscillations of both longitudinal mode and Rayleigh mode for the water-brass interface in this work. It should be noted that the grating equation only describes the common feature of

the energy radiation of surface resonance, i.e. surface resonance of all modes propagating back to the receiver, but this feature is not necessarily the whole picture of the energy radiation of surface resonance. For example, the surface resonance of longitudinal mode observed from the water-brass interface in this work behaves like a point source radiating its energy to the whole diffraction field.
(iv) Virtual interference between direct reflection and the surface resonance radiated back to the receiver. The reflection signal received by the receiving transducer contains both the direct reflection (main bang of the reflection waveform) and the radiated surface resonance (oscillating tail of the reflection waveform) from the corrugated surface. Because these two parts of the reflection signal are separated from each other in time domain waveform, a phase difference must exist between the radiated surface oscillations and the components of the direct reflection that has the same frequency as the surface oscillations. In the frequency domain representation of the whole reflection signal, i.e. the reflection spectrum, this phase difference will result in either a spectral dip (phase cancelling effect) or spectral peak (phase enhancing effect), or even both. These spectral anomalies are then identified as acoustic Wood anomalies. It should be noted that the two parts of the reflection signal do not physically interfere with each other in both time domain and space domain. Therefore, a spectral dip (or a spectral tip) in the reflection spectrum is not the representation of an actual destructive interference (or constructive interference), but a virtual one generated by the data processing method FFT.

### 2.3.4 Additional Experiments

In the above discussions the results obtained from the corrugated water-brass interface are used for illustration, while in this section the results obtained from the corrugated brass-water interface and brass-air interface will be shown and discussed.

### 2.3.4.1 Spectral Anomaly of Brass-Water Interface

The waveforms of the reflections from the flat and corrugated brass-water interface are compared in Figure 2-8 (a), and their spectra are compared in Figure 2-8 (b). The sonograms of the flat and corrugated surface reflections are shown in Figure 2-8 (c) and (d) respectively.

A spectral dip appearing at 10.89 MHz can be identified through the spectrum comparison as shown in Figure 2-8 (b). Because the frequency of this spectral anomaly is the same as that of the spectral tip observed for the corrugated water-brass interface, it is logical to conclude that they have the same physical origin. In other words, this spectral dip also corresponds to the generation of the surface resonance at the transition between the propagating mode of incident wave in brass and the evanescent mode of Rayleigh-like surface wave at the interface. The generation of the surface resonance can be proved by both the existence of oscillations in the tail of the reflection shown in Figure 2-8 (a) and the observation of the time-frequency distribution of the reflection tail shown in Figure 2-8 (d). The difference between the current anomaly and that for the water-brass interface is that the anomaly in the reflection from the corrugated water-brass interface is a spectral tip resulting from the phase enhancing effect between the main bang and the oscillating tail of the specular reflection, while the anomaly in this case is a spectral dip resulting from the phase cancelling effect.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-053_1746_1362_274_351.jpg)

Figure 2-8 Comparison of the reflections from flat and periodically corrugated brass-water interfaces: (a) waveforms, (b) amplitude spectra, (c) sonogram of flat interface reflection, and (d) sonogram of corrugated interface reflection.

### 2.3.4.2 Spectral Anomaly of Brass-Air Interface

The waveforms, spectra and sonograms of the reflections from flat and corrugated brass-air interfaces are shown and compared in Figure 2-9. Because both brass-air
interface and brass-water interface belong to the same general interface category of solid-liquid interface, they share the similar physical principles that govern the interface interaction between ultrasound and surface corrugation, and therefore have the similar results. This can be confirmed by comparing Figure 2-8 and Figure 2-9.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-054_1571_1357_767_361.jpg)

Figure 2-9 Comparison of the reflections from flat and periodically corrugated brass-air interfaces: (a) waveforms, (b) amplitude spectra, (c) sonogram of flat interface reflection, and (d) sonogram of corrugated interface reflection.

The anomaly frequency in this case is 10.87 MHz and it is a little bit smaller than the anomaly frequency (10.89 MHz) observed from brass-water and water-brass interfaces. The percentage difference between these two anomaly frequencies is only 0.2% and they can be treated as the same value considering the possible error in the experimental operation. It should be pointed out that the spectral dip for the brass-air interface is much sharper and deeper than that obtained from brass-water interface, which indicates that the surface resonance generated in this case is relatively stronger than that generated at brass-water interface. This indication can be confirmed by comparing the sonogram for brass-water interface in Figure 2-8 (d) and the sonogram of brass-air interface in Figure 2-9 (d). The reason for this difference lies in the fact that the reflection coefficient of brass-air interface is larger than that of brass-water interface and therefore more energy, including the energy of surface resonance, is reflected back to the receiving transducer in the case of brass-air interface under the same experimental conditions.

### 2.4 Conclusions

In this work the physical origin of the acoustic Wood anomaly observed in the specular reflection spectrum from corrugated interfaces is investigated. The experimental investigation is performed on a brass sample with a periodically corrugated surface of a rectangular profile. In order to make a complete and conclusive investigation specular reflections from all three basic types of corrugated interfaces, namely, liquid-solid interface, solid-liquid interface and solid-air interface, are obtained for analysis. The existing assumptions and explanations concerning the acoustic Wood anomaly phenomenon are reviewed, examined and evaluated based on the analysis of the experimental results obtained in this work. And a relatively complete explanation for the physical origin of acoustic Wood anomaly has been finally reached.

One of the contributions of this work is the observation of a spectral tip from the
reflection spectrum of the water-brass interface. Although a similar spectral anomaly has been observed in Wood’s original work [20] for optics, it has never been reported in acoustics. In this work time-frequency domain analysis is introduced into the analysis of acoustic Wood anomaly for the first time. The resultant sonogram of the specular reflection from a corrugated interface points out the commonly accepted false assumption about the acoustic Wood anomaly, in which a spectral dip is interpreted as energy loss, by showing the wave energy at anomaly frequency is not missing from the specular reflection as many researchers believed, but only retarded. Another fact that has never been pointed out in the literature before, but emphasized by this work is that the spectral dip is not an actual destructive interference, but a virtual one caused by the data processing method (FFT) because the signals, which are thought as to interfere with each other, are actually separated in the time domain as observed in this work. In fact, the phase difference between the temporally separated signals plays a central role in the occurrence of spectral anomalies: a spectral dip is the result of a phase cancelling effect, while a spectral tip is the result of a phase enhancing effect.

## RESUME DU CHAPTRE III

Un réseau de diffraction est un filtre spatial qui réfléchit les ondes sonores ou les ondes optiques afin de tenir compte dans les directions déterminées par la fréquence et par la périodicité du réseau de diffraction. Fait intéressant, le phénomène peut être très bien décrit à partirde en utilisant du technique de transformée de Fourier discrète, fondamentalement construite sur l’hypothèse de base que la plus petite période identifiable est le descripteur de base de la fonction étudiée. La série de Fourier pouvant être obtenue est alors la somme des fonctions harmoniques ayant chacune une périodicité égale à une fraction entière du descripteur de base, mais jamais d’un multiple. Ici, nous montrons, au moyen d’expériences acoustiques, qu’en réalité, un multiple du descripteur de base doit être inclus, provoque un nouveau type de diffraction sous-harmonique, en plus de la diffraction harmonique bien connue. Cette découverte ouvre la possibilité de mieux concevoir les spectres de diffraction spatiale, comme un effet arc en ciel, sans la limitation de la séquence de couleur traditionnelle.

## CHAPTER III  SUB-HAMONIC DIFFRACTION PHENOMENON

### 3.1 Introduction

A diffraction grating as a spatial filter, which reflects the constituting components of an incident beam to different directions according to their frequency and the periodicity of the grating, has been intensively studied in both optics [1-5] and acoustics [6-9]. The classical grating equation is the rule of thumb in describing the relationship between the directions of the diffracted waves of different orders and their corresponding frequencies at a given incident angle for a grating with a given periodicity. Most of experimentally observed phenomena can be well explained by the classical grating equation. The periodicity in the classical grating equation is the smallest identifiable periodicity, i.e., fundamental periodicity, of a given corrugation, neither a fraction of the fundamental periodicity nor a multiple of it. However, in the current study the experimentally obtained diffraction fields go beyond what the classical grating equation is capable of explaining, and an extended grating equation with a multiple of the fundamental periodicity introduced has been employed in order to successfully explain the experimental observations.

The main purposes of this work are to report the experimental results of the diffraction fields of both periodically corrugated silicon samples and brass samples obtained in Bragg diffraction configuration and in general diffraction configuration, and to investigate the possible physical causes of the observed phenomenon. In the rest of this chapter the details of the experimental investigation are first presented. The experimentally observed diffraction phenomenon from Bragg diffraction configuration that can be perfectly explained by the classical grating equation and its theoretical
foundation is followed. Then, the experimentally observed diffraction phenomenon that cannot be explained by the classical grating equation, i.e., the so-called sub-harmonic diffraction phenomenon, is presented. The internal reflection within the corrugation structures, which is considered as an important factor that can possibly cause this phenomenon, is discussed. Other factors that possibly cause the sub-harmonic phenomenon such as the finite beam width and imperfect corrugation periodicity are also discussed. In order to explain the experimental observation an extension is made to the classical grating equation by incorporating an integer coefficient into the equation. For the purpose of checking the generality of this phenomenon the experimental results obtained from general diffraction configuration are also demonstrated. Furthermore, the similar phenomenon that possibly occurs in optics is predicted and shown in simulated diffraction spectra.

### 3.2 Samples and Experimental Setup

### 3.2.1 Samples

Two sets of samples are investigated in this study. The first set of samples contains four silicon disks with periodically corrugated structures on one side. Two of the silicon samples (Silicon I and II) have one-dimensional corrugation, while the other two (Silicon III and IV) have two-dimensional corrugation. The corrugation structures of Silicon I and II shown in Figure 3-1 (a) and (b) respectively, have the same periodicity, but different height; the corrugation structure of Silicon III is pillars as shown Figure 3-1 (c) and that of Silicon IV is holes as shown in Figure 3-1 (d).

The other set of samples consists of three brass blocks with periodic profiles on their top surfaces. These three brass samples (Brass I, II and III) have one-dimensional
corrugated structures with different periodicity and height. The optical microscopic images of the corrugation structures of the brass samples are shown in Figure 3-2.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-060_1357_979_541_529.jpg)

Figure 3-1 Images of the corrugation structures of the four silicon samples: (a) Silicon I, (b) Silicon II, (c) Silicon III and (d) Silicon IV.

The corrugation structures of the silicon samples are fabricated using chemical etching technique in clean room, while those of brass samples are fabricated using mechanical machining technique in machine shop. The different fabrication techniques of the two sets of samples lead to different corrugation quality in terms of surface smoothness and consistency in corrugation periodicity and height. The surface
smoothness of corrugation is directly related to the intensity of the diffraction field through scattering: rougher corrugation surface randomly scatters more acoustic energy leading to relatively lower diffraction intensity. In this study the silicon samples are made under the same conditions using the same technique, and therefore their corrugation structures have the same surface smoothness. Due to that chemical etching has higher accuracy than mechanical machining the corrugation of the silicon samples has higher surface smoothness than that of the brass samples.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-061_996_931_1015_553.jpg)

Figure 3-2 Images of the corrugation structures of the three corrugated brass samples: (a) Brass I, (b) Brass II, (c) Brass III.

In order to obtain accurate values of corrugation periodicity direct measurements of 20 corrugations of each sample are performed on the optical microscopic images shown in Figure 3-1 and Figure 3-2. The corrugation height of each sample (except for Brass I) is measured using high frequency ultrasonic geometrical characterization method
[10] and the result is also based on the measurement of 20 corrugations. The average value (A) and the ratio of standard deviation to average (SD/A) are obtained for both corrugation periodicity $(\Lambda)$ and height $(\mathrm{H})$. The ratio of corrugation periodicity to height $(\Lambda / \mathrm{H})$ is also given for later discussion. All the dimensional parameters of the samples are listed in Table 3-1. The fact that the values of SD/A of corrugation periodicity and height of the silicon samples are much smaller than those of the brass samples suggests that the silicon samples have higher consistency in corrugation periodicity and height.

Table 3-1 Dimensional parameters of the corrugated samples: corrugation periodicity $(\Lambda)$, corrugation height (H), their average (A), the ratio between standard deviation and average (SD/A), the ratio of corrugation periodicity to height ( $\mathbf{\Lambda} \boldsymbol{/} \mathbf{H}$ ), and the total thickness (T).
| Sample | $\Lambda$ | | H | | $\Lambda / \mathrm{H}$ | $\mathrm{T}[\mu \mathrm{m}]$ |
| :— | :— | :— | :— | :— | :— | :— |
| | A $[\mu \mathrm{m}]$ | SD/A [%] | $\mathrm{A}[\mu \mathrm{m}]$ | SD/A [%] | | |
| Silicon I | 100 | 0.8 | 187 | 0.4 | 0.53 | 500 |
| Silicon II | 100 | 1.0 | 27 | 1.4 | 3.70 | 500 |
| Silicon III | 100 | 0.7 | 195 | 0.7 | 0.51 | 500 |
| Silicon IV | 100 | 0.6 | 172 | 0.4 | 0.58 | 500 |
| Brass I | 180 | 3.4 | 25* | 7.4 | 7.20 | 11820 |
| Brass II | 305 | 1.7 | 94 | 3.9 | 3.24 | 11780 |
| Brass III | 511 | 2.2 | 253 | 5.2 | 2.02 | 12750 |

[1](about:blank#fn1)In addition, the total thicknesses of all the samples are measured using digital caliber and also listed in Table 3-1. It can be seen that brass samples have high thickness values and the advantage of these high values is that the reflections from the other side of the sample can be eliminated by setting a window of proper length when acquiring the time-domain diffracted signals. The silicon samples, however, do not
have this advantage and the reflected signals from the other side of the sample will combine with the acoustic signals diffracted by the corrugated structures. But due to the huge difference of the characteristic acoustic impedance between water and silicon at room temperature, theoretically 90.6% of the incident power is reflected back into the water at the water-silicon interface; and only about 0.8% of the incident power could possibly go back into the water and combine with the diffracted signals after being reflected by the other side of the sample and transmitting through the corrugated surface again. Therefore, it is safe to use the silicon samples to study the diffraction phenomenon.

### 3.2.2 Transducer Selection

Five commercial immersion transducers are used in this study in order to confirm the repeatability of the diffraction phenomenon observed. For each transducer the central frequency and the diameter of active piezoelectric element provided by the manufacturers, and the spectral coverage obtained in the spectrum of an echo reflected from a smooth brass surface are provided in Table 3-2.

It has been shown that the results obtained using the transducers of different frequencies confirm each other in their respective spectral coverage. Since the transducer with a central frequency of 20 MHz has the largest spectral coverage, only the results obtained using this transducer are shown in this paper.

Table 3-2 Basic parameters of the immersion transducers used in this study.
| Central Frequency [MHz] | 5 | 10 | 15 | 20 | 25 |
| :— | :— | :— | :— | :— | :— |
| Diameter [mm] | 12.7 | 12.7 | 9.5 | 6.4 | 6.4 |
| Spectral Coverage [MHz] | 2.1-7.5 | 5.2-12.3 | 1.5-19.5 | 1.2-30.5 | 1.9-23.5 |

### 3.2.3 Experimental Setup and Procedures

Two experimental configurations are applied in this work: Bragg diffraction configuration (Figure 3-2 (a)) and general diffraction configuration (Figure 3-2 (b)). In acoustics the so-called Bragg diffraction refers to the diffraction phenomenon in which the diffracted wave is backscattered onto the emitting transducer [11] and it shares the same mathematical expression as Bragg diffraction in optics. Being consistent with the experimental configuration shown in Figure 3-2 (a) the mathematical expression of Bragg diffraction in this study is taken the following form:

$$
\sin \theta_{\text {Bragg }}=m \frac{c}{2 f \Lambda}
$$

with $\theta_{\text {Bragg }}$ as the (Bragg) angle of diffraction, $m$ the order of diffraction, $c$ the sound speed in water, $f$ the frequency of sound, $\Lambda$ the corrugation periodicity. In Bragg diffraction configuration only one transducer is used and this transducer works as both an emitter and a receiver. In this work a symmetric polar scan from $-60^{\circ}$ to $+60^{\circ}$ with respect to the normal position of the corrugated surface (0° position) is performed.

The mathematical expression of general diffraction configuration is taken the following mathematical form:

$$
\sin \theta_{m}=\sin \theta_{i n c}+m \frac{c}{2 f \Lambda}
$$

with $\theta_{m}$ as the angle of the $\mathrm{m}^{\text {th }}$ order diffraction, $\theta_{\text {inc }}$ the angle of incidence. Equation (3-2) is the general form of sound diffraction by corrugated structures with a random angle of incidence, and Bragg diffraction is just its special case in which the incident angle coincides with the diffraction angle. In the general diffraction configuration two
transducers are used, one working as an emitter and one as a receiver. In this work three incident angles (-30°, -10° and 0°) are investigated and the corresponding diffraction fields are scanned within a proper range.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-065_1407_941_628_541.jpg)

Figure 3-3 Schematics of experimental setup: (a) Bragg diffraction configuration and (b) general diffraction configuration.

In this study we mainly focus on Bragg diffraction configuration and the reasons are (i) this configuration is simple and efficient because the total investigation can be done in one scan using one transducer; and (ii) the results obtained in this configuration is
relatively accurate compared with those obtained in general diffraction configuration because it is easy for the beam to focus on a specific area of corrugation during the scan process, i.e. less disturbance originating from testing area change involved; (iii) the wave generation and acquisition is through the same piezoelectric material which increase the signal reliability. However, Bragg diffraction is just a special case of general diffraction, and the results obtained in general diffraction configuration are still needed in order to check the generality of the diffraction phenomenon observed.

The scan is performed using a customer-designed ultrasonic scanner fabricated by ‘Inspection Technology Europe BV’. Data acquisition is completed using ‘Winspect’ software package, and further data processing is performed using ‘Matlab’.

### 3.3 Perfect Diffraction

In this section we first demonstrate the experimental evidences of Bragg diffraction that perfectly match the theoretical expectation based on the classical grating equation, and then we review the theoretical origin of the grating equation.

### 3.3.1 Bragg Diffraction of Silicon Samples

The angular spectrograms of Silicon III and IV shown in Figure 3-4 are obtained through Fourier transform of angle-time domain signals acquired from a polar scan in Bragg diffraction configuration. As mentioned in the previous section the results obtained using the transducers of different frequencies confirm each other, and so only those obtained using the 20MHz transducer are shown here.

Although Silicon III and IV have two-dimensional corrugation structures, they function as one-dimensional corrugation in the experiments due to that only onedimensional scan is performed and accordingly only one-dimensional diffraction effect
is acquired. The only difference these functionally one-dimensional corrugations have, compared with the real one-dimensional corrugations with the same corrugation periodicity and height, is that the intensity of diffraction is lower because they have less area to generate the reflection diffraction that can be experimentally detected.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-067_1155_1056_751_479.jpg)

Figure 3-4 Angular spectrogram of the Bragg diffraction field of (a) Silicon III and (b) Silicon IV obtained using a 20 MHz transducer.

In the angular spectrogram of Silicon III seven orders of Bragg diffraction can be clearly observed: 0 order diffraction (specular reflection) positioned at zero degree for all the possible frequencies, three negative orders on left-hand side of the specular reflection, and three positive orders on the right-hand side of the specular reflection. As predicted by the governing equation (Equation 3-1) the negative order diffractions are
symmetric to the positive order diffractions. The same observation can be made from the angular spectrogram of Silicon IV except for the +3 order of diffraction is too weak to be seen. These are two examples that the experimentally obtained diffraction perfectly match their corresponding theoretical expectation based on the classical grating equation for Bragg diffraction as Equation (3-1).

### 3.3.2 Theory Based on Fourier

The classical grating equation in optics and in acoustics can be found in standard textbooks in one form or another, though always equivalent to its wavenumber form:

$$
k_{x}=k_{x}^{i n c}+m \frac{2 \pi}{\Lambda}
$$

To understand the theoretical origin of this equation one must consider Fourier analysis of periodic functions. A function $f(x)$ is periodic with a period $\Lambda$ if

$$
f(x)=f(x+\Lambda)
$$

A Fourier series is essentially a decomposition of a periodic signal into orthogonal functions. When a periodic function $f(x)$ is decomposed into orthogonal functions, these functions should also be periodic, such that

$$
f(x)=\sum_{-\infty}^{+\infty} A_{m} g_{m}(x)=\sum_{-\infty}^{+\infty} A_{m} g_{m}(x+\Lambda)=f(x+\Lambda)
$$

In other words, if $g_{m}$ are harmonic functions we have

$$
g_{m}(x)=\exp i\left(k_{m} x\right)=\exp i\left(k_{m} x+k_{m} \Lambda\right)=g_{m}(x+\Lambda)
$$

This is true when

$$
k_{m} x=k_{m} x+k_{m} \Lambda-2 m \pi
$$

hence,

$$
k_{m}=m \frac{2 \pi}{\Lambda}
$$

This must also be true for $\Lambda$ being infinite (plane surface) which means, taking into account Snell’s law, the condition for the total sound field $f(x)$ results in:

$$
k_{x}=k_{x}^{i n c}+m \frac{2 \pi}{\Lambda}
$$

### 3.4 Sub-harmonic Diffraction

In this section the sub-harmonic diffraction phenomena observed from the diffraction fields of Silicon I and II are first presented and analyzed, the investigation of theoretical explanation is followed, and then the results obtained from brass samples are demonstrated.

### 3.4.1 Bragg Diffraction of Silicon Samples

The angular spectrograms of Silicon I and II are shown in Figure 3-5. Because all the corrugated silicon samples have the same periodicity, Silicon I and II are expected to have the same diffraction pattern as Silicon III and IV. The observation of the diffraction field of Silicon I in Figure 3-5 (a) shows that the diffraction fringes with high intensity confirm this expectation. However, in between the adjacent diffraction fringes expected based on acoustic Bragg diffraction there are three other diffraction fringes that have neither been observed in Figure 3-4, nor been predicted by the grating equation.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-070_1217_1095_361_462.jpg)

Figure 3-5 Angular spectrogram of the Bragg diffraction field of (a) Silicon I and (b) Silicon II obtained using a 20 MHz transducer.

Taking the angle-frequency data from all the diffraction fringes observed in Figure 3-5 (a) and putting them back into acoustic Bragg diffraction equation (Equation (3-1)) the values of diffraction orders in decimal format are obtained and listed in Table 3-3. Because all the angle-frequency data obtained from the same diffraction fringe give the same value of diffraction order, only one set of angle-frequency wave is obtained from each diffraction fringe for calculating the value of diffraction order. It can be observed that the data is symmetric around zero and this is due to the symmetry of the diffraction pattern. It can also be observed that the difference between all the adjacent values is
0.25 (1/4 in fraction format) and this inspires us to represent all the data in fraction format with a denominator of 4. All the fractional data are also listed in Table 3-3 and it can be seen that their numerators are consistent integers ranging from -12 to +12.

Table 3-3 Values of all possible diffraction orders obtained based on experimental results and the classical grating equation for Silicon I.
| Decimal | -2.97 | -2.72 | -2.49 | -2.23 | -1.97 | -1.73 | -1.47 | -1.24 | -0.98 | -0.73 | -0.49 | -0.25 | 0.00 |
| :— | :— | :— | :— | :— | :— | :— | :— | :— | :— | :— | :— | :— | :— |
| Format | 2.98 | 2.72 | 2.47 | 2.23 | 2.00 | 1.75 | 1.49 | 1.24 | 1.00 | 0.75 | 0.50 | 0.25 | |
| Fractional | -12/4 | -11/4 | -10/4 | -9/4 | -8/4 | -7/4 | -6/4 | -5/4 | -4/4 | -3/4 | -2/4 | -1/4 | 0/4 |
| Format | 12/4 | 11/4 | 10/4 | 9/4 | 8/4 | 7/4 | 6/4 | 5/4 | 4/4 | 3/4 | 2/4 | 1/4 | |

Obviously the above observation cannot be explained by the classical grating equation because of its requirement that the diffraction order $m$ must be an integer. Based on the experimental data it is definite that the denominator 4 is not a random number and that there must be some reason behind that we have not yet found. If we call the diffraction fringes with integer orders harmonic diffraction, it is proper to call the newly observed diffraction fringes in between the harmonic diffractions subharmonic diffraction. Actually, this phenomenon can also be observed from the result of Silicon II shown in Figure 3-5 (b), although it is not as clear as in Figure 3-4 (a). Furthermore, even for the diffraction of Silicon III and IV (Figure 3-4) this phenomenon can be observed although the intensity of sub-harmonic diffraction is too low to be clearly visible.

### 3.4.2 Adjustment of Grating Equation to Incorporate Internal Reflections

There are two major geometrical parameters for corrugation structures: periodicity and height. In the classical grating equation corrugation periodicity is considered, but
corrugation height is not. Therefore, when attempting to find the reasons behind the sub-harmonic diffraction phenomenon the possible effect of corrugation height is focused on. When sound incident onto a corrugation structure some of the incident energy is reflected directly by the higher surfaces, while some of the energy is temporarily trapped by the tunnels formed by two adjacent corrugation components. The trapped energy propagates within the tunnel forming internal scattering and the time duration of this internal scattering mainly depends on the corrugation height.

When internal scattering occurs the waves coming out of the grooves (when reflected or transmitted) obtain an extra phase change related to their elongated propagation path. This phase change is not considered when the classical grating equation is used. Diffraction in this case will be due to recombination of waves (from the top of the grooves) with waves that are ahead in phase and coming from the bottom of the grooves. This is taken into account when the classical grating equation is replaced by

$$
k_{x}=k_{x}^{i n c}+\frac{2 m \pi}{p \Lambda}
$$

where $p$ is a real number. When the width of a groove is half the periodicity of the corrugation, it is expected that $p$ is an integer.

Applying this extended grating equation to the sub-harmonic diffraction observed in Figure 3-5 we can see that the number $p$ is the integer 4 for Silicon I and II.

### 3.4.3 Bragg Diffraction of Brass Samples

The sub-harmonic diffraction is not only observed in silicon samples, but also in brass samples. Figure 3-6 shows the angular spectrograms of Brass I, II and III based on the data obtained in Bragg diffraction configuration using a 20 MHz transducer. The
sub-harmonic diffraction phenomenon can be clearly observed for Brass I in Figure 3-6 (a) and Brass III in Figure 3-6 (c), while for Brass II no obvious sub-harmonic diffraction can be seen from Figure 3-6 (b) although there is some signal in between the major diffraction fringes.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-073_1768_1061_657_469.jpg)

Figure 3-6 Angular spectrogram of the Bragg diffraction field of (a) Brass I, (b) Brass II and (c) Brass III obtained using a 20 MHz transducer.

The sub-harmonic diffraction of Brass I in Figure 3-6 (a) has a clear pattern, especially in between the -1 order and +1 order of diffraction. Using the same analyzing technique as the one applied to Silicon I (Figure 3-5 (a)) the diffraction fringes in between -1 order and +1 order are analyzed and the results are shown in Figure 3-7. In order to check the symmetry of the positive and negative orders only their absolute values are plotted. It can be seen that all the data fall into 7 groups: upper left group from -1 order diffraction, lower middle group from 0 order diffraction, upper right group from +1 order diffraction, and all the other four groups from the so-called sub-harmonic diffraction. The symmetry between the positive and negative orders can be observed although it is not as perfect as that of Silicon I shown in Table 3-3.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-074_789_1155_1313_445.jpg)

Figure 3-7 Absolute values of all possible diffraction orders from -1 to +1 order of Bragg diffraction. The values are extracted based on experimental data and classical grating equation.

It should be noted that the sub-harmonic diffraction observed for Brass I is not exactly like that for silicon sample in terms of existence of a fix $p$ value. The only
denominator that is found to make all the numerators of the extracted diffraction orders as consistent as possible is 18. All the extracted data of possible diffraction orders are listed in Table 3-4. From both Figure 3-7 and the fractional format representation of the data in Table 3-4 it can be observed that the diffraction orders between 0 order and ±1 order diffractions fall into two groups and this observation can be confirmed by the diffraction between ±1 order diffractions of Brass III in Figure 3-7 (c). This inspires us to guess that the possible number of $p$ for Brass I might be 3 and that this number is possibly related to corrugation material.

Table 3-4 Values of all possible diffraction orders obtained based on experimental results and the classical grating equation for Brass I.
| Decimal Format | -1.10 | -1.05 | -0.99 | -0.86 | -0.77 | -0.71 | -0.66 | -0.61 | -0.44 | -0.39 |
| :— | :— | :— | :— | :— | :— | :— | :— | :— | :— | :— |
| | -0.32 | -0.27 | -0.23 | -0.06 | 0.00 | 0.05 | 0.27 | 0.33 | 0.38 | 0.44 |
| | 0.48 | 0.59 | 0.65 | 0.71 | 0.77 | 0.83 | 0.98 | 1.04 | 1.13 | |
| Fractional Format | -20/18 | -19/20 | -18/18 | -15/18 | -14/18 | -13/18 | -12/18 | -11/18 | -8/18 | -7/18 |
| | -6/18 | -5/18 | -4/18 | -1/18 | 0/18 | 1/18 | 5/18 | 6/18 | 7/18 | 8/18 |
| | 9/18 | 11/18 | 12/18 | 13/18 | 14/18 | 15/18 | 18/18 | 19/18 | 20/18 | |

### 3.5 Discussions

In last section the internal reflection within the corrugation is considered as the source of the observed sub-harmonic diffraction by adjusting the expression of grating equation. In this section other possible explanations for the existence of sub-harmonic diffractions are investigated and the factors that possibly affect the pattern of such diffraction are also discussed.

### 3.5.1 Wrong Fourier Theory

Let us play the devil’s advocate for a moment. When a function $f$ is translated by an amount (a number times $\Lambda$ ) it does not alter. In other words

$$
f(x)=f(x+p \Lambda)
$$

This means that when $f$ is decomposed into orthogonal functions, these functions should also meet those requirements such that

$$
f(x)=\sum_{-\infty}^{+\infty} A_{m} g_{m}(x)=\sum_{-\infty}^{+\infty} A_{m} g_{m}(x+p \Lambda)=f(x+p \Lambda)
$$

In other words, if $g_{m}$ are harmonic functions we have

$$
g_{m}(x)=\exp i\left(k_{m} x\right)=\exp i\left(k_{m} x+p k_{m} \Lambda\right)=g_{m}(x+p \Lambda)
$$

This is true when

$$
k_{m} x=k_{m} x+p k_{m} \Lambda-2 m \pi
$$

hence

$$
k_{m}=\frac{2 m \pi}{p \Lambda}
$$

This must be true also for $\Lambda$ being infinite (plane surface) which means, taking into account Snell’s law, the condition for the total sound field $f(x)$ results in:

$$
k_{x}=k_{x}^{i n c}+\frac{2 m \pi}{p \Lambda}
$$

This is the same equation as Equation (3-10). It seems to prove that in a Fourier series one should not take the fundamental period but any multiple of that fundamental period. It would result in a conclusion that the existing Fourier theory is incomplete and must be expanded.

At this point we stop playing the devil’s advocate. If the above statements related to Fourier analysis were correct, it would involve interactions of sound over large distances along the corrugated interface. For plane waves it is hard to prove the contrary, however in this paper, as always in real situations, all experiments are done using bounded beams. If long distance interaction were the physical reason behind Equation (3-10), the experimental results would highly depend on the diameter of the used bounded beams. As shown in Table 3-2 three different diameters of bounded beam are investigated in this study and they all give the same results in terms of the appearance of sub-harmonic diffraction and the diffraction pattern for all the samples. We can conclude that the beam diameter does not influence the appearance or disappearance of diffraction fringes. This means that long distance interactions can be excluded and Equation (3-10) is not a result of classical Fourier analysis being wrong, but possibly due to internal reflections as suggested above.

### 3.5.2 Imperfect Periodicity

The periodicity of corrugation is a critical factor to diffraction phenomenon. In this study the quality of corrugation periodicity is indicated by the ratio of standard deviation to average value (SD/A) shown in Table 3-1. It can be seen (i) that all the four silicon samples have highly consistent corrugation periodicities, (ii) that the brass samples have less perfect periodicity than silicon samples, and (iii) that among the
three brass samples Brass I has the least periodicity consistency and Brass II has the best.

Referring to Figure 3-6 it seems that the periodicity consistency is related to the appearance of sub-harmonic diffraction: Brass I has the largest SD/A value (3.4%) and it has sub-harmonic diffraction with relatively clear pattern; Brass III has the second largest SD/A value (2.2%) and it also has sub-harmonic diffraction but with less clear pattern; and Brass II has the least SD/A value (1.7%) and its sub-harmonic diffraction is barely visible. However, when comparing the brass samples to the silicon samples we can see that the periodicity consistency is not necessarily the determining factor for the appearance of sub-harmonic diffraction because the silicon samples have more clear sub-harmonic diffraction pattern than the brass samples although their periodicity consistency is much higher.

### 3.6 General Diffraction Experiment

Up to now all the experimental evidences shown for sub-harmonic diffraction are obtained from Bragg diffraction configuration. The natural question arises: is it only a Bragg diffraction phenomenon, or it applies to more general diffraction situations? The experiments performed under the general diffraction configuration at three randomly chosen incident angles ( $-30^{\circ},-10^{\circ}$ and $0^{\circ}$ ) for all the samples support the existence of sub-harmonic diffraction and two examples are shown in Figure 3-8.

The first example shown in Figure 3-8 (a) is from a silicon sample. The fringe with high intensity is +1 order diffraction and the other three visible fringes correspond to the orders 1/4, 2/4 and 3/4 according to the calculation. This proves that for silicon samples the number $p$ in the extended grating equation (Equation (3-10)) is 4. The example shown in Figure 3-8 (b) is from a brass sample. From the left to the right the
high intensity diffraction fringes correspond to -1, 0 and +1 order diffractions. In between these orders of diffraction there are other fringes although they do not show any clear pattern as those of silicon samples do.

It should be noted that the diffraction fringes obtained in general diffraction configuration are not as good as those obtained in Bragg diffraction configuration because (i) it is difficult for the emitter and the receiver to exactly focus on the same position of the corrugation and (ii) the emitter and the receiver have slightly different sensitivity to the same signals.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-079_1239_1116_1119_445.jpg)

Figure 3-8 Angular spectrogram of the general diffraction field of (a) Silicon II with an incidence angle of -10° and a polar scan range of 30° to 90°, and (b) Brass I with an incidence angle of -30° and a polar scan range of -20° to 90° obtained using a 20 MHz transducer.

### 3.7 Prediction of Sub-harmonic Diffraction in Optics

Since the sub-harmonic diffraction can be observed in acoustical diffraction, it is possible to be observed in optics, too. In this section simulation of the diffraction spectrum of a white light normally incident onto a grating with a periodicity of 700 nm is performed. Considering the light wavelength ranging from 380 nm to 700 nm the maximum value of diffraction order falls into the range of 1 to 1.84 for a normal incident white light according to the classical grating equation. This means for a diffraction with an order not larger than 1 the whole visible spectrum will be diffracted; for a diffraction with an order within 1 and 1.84 only part of visible light will be diffracted; and for a diffraction with an order larger than 1.84 no visible light can be diffracted.

The first simulation is based on classical grating equation shown in Equation (3-2). The only possible order of diffraction for the grating of 700 nm is 1 based on the above analysis. The simulation of the spatial diffraction spectrum is shown in Figure 3-9.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-080_580_1167_1791_436.jpg)

Figure 3-9 Simulation of the spatial diffraction spectrum of a white light normally incident onto a grating with a periodicity of 700 nm based on the classical grating equation.

If the sub-harmonic diffraction is considered in the simulation, the diffracted spectrum will definitely be different. In order to show the effect of sub-harmonic diffraction on spatial diffraction spectrum of visible light as well as to keep the demonstration simple the number $p$ of Equation (3-10) is chosen as 2. Thus all the possible diffraction orders that could possibly be observed are 1/2, 1 and 3/2. The diffractions with an order of 1/2 and 3/2 are shown in Figure 3-10 (a) and (b) respectively and the combination of the diffractions with all the three possible orders is shown in Figure 3-10 (c).

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-081_946_1213_1115_420.jpg)

Figure 3-10 Simulation of the spatial diffraction spectrum of a white light normally incident onto a grating with a periodicity of 700 nm: (a) diffraction of order 1/2; (b) diffraction of order

$\frac{\mathbf{3}}{\mathbf{2}}$

; and (c) combination of the diffractions of order 1/2, 1 and 3/2.

### 3.8 Conclusions

The experimental observation in this work confirms the validity of classical grating equation in acoustic diffraction. Beyond that new diffraction phenomenon called sub-
harmonic diffraction is observed. Due to the fact that classical grating equation is invalid in explaining the origin of this observation, theoretical investigation is performed and an extended grating equation is reached mainly by considering the effect of the internal reflections within the corrugation structures on the diffraction field. Several factors that might possibly affect the diffraction field and cause sub-harmonic diffraction are discussed. And the spatial diffraction spectrum is simulated for visible light assuming that sub-harmonic diffraction also occurs in optics.

In summary, sub-harmonic diffraction is reported in this study and a theoretical investigation of the possible theory is made although there is no explicit proof to support the new theory.

## RESUME DU CHAPTRE IV

La mesure de la périodicité du réseau de diffraction composé de tiges cylindriques empilées est effectuée à l’aide d’une technique à ultrasons couplés à l’air. La diffusion acoustique de Bragg de trois structures périodiques est étudiée au moyen d’un balayage polaire. Par conséquent, les angles de Bragg et les fréquences correspondantes sont obtenus à partir de spectrogrammes angulaires, en utilisant deux approches d’acquisition de données différentes. Selon le principe de la diffraction de Bragg, les périodicités des trois structures périodiques, qui sont égales au diamètre des tiges cylindriques, sont déterminées. Afin d’évaluer la fiabilité de la technique et sa précision, les diamètres obtenus sont comparés avec ceux qui sont directement mesurés avec un calibre numérique. Afin de démontrer la robustesse de la technique experimentale, des transducteurs de qualité différente ont èté utilisés pour effectuer les mesures.

## CHAPTER IV  AIR-COUPLED ULTRASONIC INVESTIGATION OF STACKED CYLINDERICAL RODS

### 4.1 Introduction

Diffraction of an acoustic beam from a periodically corrugated interface has been intensively studied in the literature [1-5]. In this type of diffraction phenomenon the periodically corrugated surface works as a diffraction grating and the periodicity of the diffraction grating is a key factor to the diffraction pattern. When the incident beam impinges the grating at a specific angle called ‘Bragg angle’, a reflected beam is backscattered to the beam source. Even though William Laurence Bragg and William Henry Bragg studied this phenomenon for the case of diffraction of X-rays in crystals [6] and not for ultrasonic waves on periodic surfaces, the formula they obtained (the ‘Bragg condition’) is equal to the grating equation applied to back-reflected sound in acoustics. This will become clear in later sections where a theoretical derivation is outlined. Bragg scattering has first been explored for X-rays diffracted by a crystal structure and since then it has been applied to measurement and characterization in a variety of areas [7-9], including ultrasonics [9-11] and underwater acoustics [12-14]. Acoustic Bragg scattering occurring at the interfaces of air and liquid [15], liquid and solid [16] and liquid and liquid [17] for instance have been explored in the past. Even Bragg diffraction of surface acoustic waves [18, 19] has been subject to investigations in the past and has shown promising application in transducers. Acoustic Bragg scattering often occurs in phononic crystals on which studies and relevant applications attempt to exploit band gaps for noise reduction or other acoustic effects [3-5, 20, 21]. In acousto-optics [22, 23] laser light at the optical Bragg incident angle and under the acousto-optic Bragg regime is applied for
many applications such as filtering of light, switching of light, steering of light and even for acousto-optic imaging of materials [24].

In manufacturing industries the dimension of final products such as the diameter of cylindrical rods is an important factor for the product quality and, therefore, is of great interest for quality control and monitoring. On the transportation line and during storage the products are often stacked and form a periodic structure. This enables the possibility to measure their periodicity, and hence their size. Earlier the possibility of measurement of the periodicity of immersed periodic structures based on Bragg scattering was explored theoretically [25] for a corrugated solid immersed in a liquid; the current experimental study explores the technique for a practical application and is based on aircoupled ultrasound.

The spaghetti and pasta industry in general is a continuously developing industry and as a consequence a significant amount of research papers appear annually on different aspects of this product [26-30]. Important for quality control of pasta is the ability of investigations in a dry and clean environment avoiding immersion or direct contact. For this purpose air coupled ultrasound [31-33] is a very inviting tool. Air-coupled ultrasound has been studied for different applications such as for instance nondestructive testing (NDT) of composites [34-37], NDT of textiles [38], NDT of lumber [39] and NDT of specific structures such as plates [40] or big composite rods [41].

The paper is structured as follows. First is explained what the Bragg angle is and how it is related to the frequency and to the rod diameter. Then the sample preparation, transducer selection and the experimental setup are outlined. Consequently the experimental method is outlined followed by a thorough description and explanation of the results.

### 4.2 Theoretical Considerations

A bounded acoustic beam in air with a sound velocity $v$ is incident onto a periodically structured solid structure with lateral spatial periodicity $\Lambda$. The beam is considered time-harmonic with frequency $f$. An example of the diffraction pattern for a beam incident onto a periodic surface is shown in Figure 4-1. All angles are given with respect to the normal of the surface. Angles, whether incident or diffracted, are taken positive on the right hand side of the normal and negative on the left hand side of the normal. According to the classical diffraction grating equation,

$$
\sin \theta_{m}+\sin \theta_{i}=m \frac{v}{\Lambda f}
$$

the diffraction angle $\theta_{m}$ of the diffracted wave of $m^{\text {th }}$ order can be obtained for a given incidence angle $\theta_{i}$. For the case of $\mathrm{m}=0$, the diffraction angle $\theta_{m}$ corresponds to the angle of the specular reflection. Positive diffraction orders m correspond to beams to the right hand side of the specular reflected beam, negative orders to the left hand side.

The Bragg angle of order $m$ is defined as the angle of incidence for which the diffracted wave is being backscattered, i.e.,

$$
\sin \theta_{i}=\sin \theta_{m}
$$

or

$$
\theta_{\text {Bragg }}=\arcsin \left(\frac{m v}{2 \Lambda f}\right)
$$

$m$ being an integer. In other words, at a Bragg angle of order $m$ the direction of the diffracted beam of order $m$ is opposite to that of the incident beam [6]. Considering the fact that in a homogenous medium like air, the sound velocity $v$ is constant and can be expressed as the product of sound frequency $f$ and wavelength $\lambda$, the conditions for the Bragg angle order $m$ to exist is as follows:

$$
|m|<\frac{2 \Lambda}{\lambda}
$$

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-087_996_1135_447_467.jpg)

Figure 4-1 Schematic of the diffraction pattern for an acoustic beam incident onto a periodic surface with a periodicity

$\Lambda$

. The incident beam, the beam of specular reflection (diffracted beam of zero order), the first positive order diffracted beam, the first and second negative order diffracted beams and their corresponding angles are shown.

In other words Bragg diffraction of order m can only exist if the wavelength is sufficiently short, i.e. at the most 2 corrugation lengths divided by m. The definition of the Bragg angle in acoustics is consistent with Bragg’s law for the case of diffraction of X-rays in crystals

$$
m \lambda=2 d \sin \theta
$$

where $m$ is an integer, $\lambda$ is the wavelength of the incident wave, $d$ is the spacing between the planes in the atomic lattice, and $\theta$ is the (Bragg) angle between the incident ray and the scattering planes.

Through a polar scan in pulse echo mode in a plane perpendicular to the stacked rods, it is possible to determine the Bragg angle. The rod diameter $\Lambda$ is obtained from Equation (4-3), i.e.

$$
\Lambda=\frac{m v}{2 f \sin \theta_{\text {Bragg }}}
$$

Note that the Bragg regime is based on the far field diffraction approach as first used by Lord Rayleigh and based on the plane wave expansion principle in the framework of Fourier series expansions [1-5]. In other regimes, not investigated here, it might be possible that other effects could be used as well such as wave front deformation due to interaction of long wavelengths with relatively small corrugations [42].

### 4.3 Samples and Experimental Setup

### 4.3.1 Sample Preparation

The motivation behind this study is to develop an experimental tool that is useful for quality control during the fabrication of pasta. For this reason three sets of commercially produced spaghetti rods, 30 rods in each set, are closely stacked in a 1-dimensional array or a 2-dimensional array. The diameters of the three sets of spaghetti rods are measured for comparison with a digital caliber. Their averages and the corresponding standard deviations and ratios of standard deviation to diameter average are given in Table I. The small ratios of standard deviation to mean for all the three sets of samples guarantee a
periodic structure of high quality with a periodicity determined by the diameter, i.e. 1.385 mm, 1.665 mm and 1.915 mm respectively.

The 1-dimensional and both 2-dimensional types of packing of the rods experimentally investigated in this study are shown in Figure 4-2.

### 4.3.2 Transducer Selection

Two air-coupled transducers of different quality and different central frequencies have been selected. Distinctive diffraction patterns require frequency bands of aircoupled transducers ensuring the Bragg angles fall within the measurable range. Bragg’s law requires that the wavelengths of acoustic waves in air are comparable with the periodicities of the investigated structures. The value of the sound velocity in air is 343 m/s, whence the wavelengths produced by the two air-coupled transducers used in the experiment are 1.559 mm (220 kHz) and 1.106 mm (310 kHz). Clearly these wavelengths are comparable to the periodicities of the three samples and ensure useful experimental data.

Table 4-1 Diameter averages and the corresponding standard deviations and ratios of standard deviation to average of the three sets of spaghetti rods.
| Set of Spaghetti Rods | Set 1 | Set 2 | Set 3 |
| :— | :— | :— | :— |
| Diameter Average [mm] | 1.385 | 1.665 | 1.915 |
| Standard Deviation [mm] | 0.018 | 0.021 | 0.020 |
| Standard Deviation/Average [%] | 1.29 | 1.26 | 1.04 |

Inasmuch as superb quality and therefore very expensive air-coupled transducers are expected to produce better experimental results, for this study we opted for relatively cheap commercially available transducers in two qualities, normally used for parking
sensor technology in automobiles, to meet the requirements for affordable mass use by the food industry.

For this research we consider a transducer producing a beam resembling Gaussian distribution in space and in the frequency domain being of better quality than more distorted beams. Therefore, the quality of the air-coupled transducers is evaluated through comparing their basic properties resembling a Gaussian beam: divergence angle and frequency dispersion range. Both of these properties are obtained from the angular spectrograms of the polar scans on a flat surface. The comparison of the angular spectrograms of 220 kHz transducer and 310 kHz transducer is shown in Figure 4-3 in which the minimum intensity is set to $1 / \mathrm{e}^{2}$ of the maximum value for the purpose of evaluation. It can be observed that the beam divergence angles are respectively 16 degrees (-6.8 to 9.2 degrees) and 30 degrees (-16.6 to 13.4 degrees), and the frequency dispersion range 36 kHz (189 to 225 kHz) and 70 kHz (260 to 330 kHz) for 220 kHz transducer respectively the 310 kHz transducer.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-090_510_512_1621_751.jpg)

Figure 4-2 Cross-sectional view of the three types of packing of rods.

Because of the fact that (i) that the extraction of diameters of the cylindrical rods is based on the major fringes and diminutive fringes of the angular spectrograms; because of the observation that (ii) the smaller the beam divergence angle is, the smaller the
major fringe is and the narrower the diminutive fringes are, and as a consequence the easier to find the angle-frequency data needed for diameter measurements; and that (iii) the smaller the frequency dispersion range is, the smaller the major fringe is, and the easier to find the angle-frequency data needed; the transducer with central frequency 220 kHz has the highest quality and the one with 310 kHz has a much poorest quality. Indicators for poor quality will be outlined when results are shown for the 310 kHz transducer.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-091_1400_1306_1044_346.jpg)

Figure 4-3 Comparison of the angular spectrograms of the polar scans on a flat surface of (a) the 220 kHz transducer and (b) the 310 kHz transducer for the purpose of transducer quality evaluation. The minimum intensity is

$\mathbf{1} / \mathbf{e}^{\mathbf{2}}$

of the maximum value.

### 4.3.3 Experimental Setup and Procedures

A single experimental setup is used in this work and all the measurements are performed in air. The experimental setup consists of a so-called polar c-scan system (Model ITE PCS22128/P) manufactured by ‘Inspection Technology Europe BV’, a pulser/receiver unit (Dual Pulser/Receiver DPR 500) manufactured by ‘JSR Ultrasonics’ and a data acquisition software ‘Winspect 6.0’. The direct measurements of spaghetti diameters are performed with a Mitutoyo digital caliber (Model No. CD-15DC). During the polar scan the transducers are set in a pulse-echo mode; the incident pulse and its frequency spectrum and the typical reflected wave and its frequency spectrum are respectively shown in Figure 4-4 and Figure 4-5.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-092_1193_1181_1251_356.jpg)

Figure 4-4 (a) Time waveform of the incident pulse of the 220 kHz transducer and (b) its frequency spectrum.

The radius of the circular track of the scanning transducers is set at $200 \mathrm{~mm}(+/-1$ mm) in order to ensure the scanned surfaces are in the far field of the emitted acoustic beams. The far field is estimated according to the empirical formula for circularly shaped transducers ${ }^{43}$ and is known to exceed the so-called Rayleigh distance $R_{0}$ with

$$
R_{0}=\frac{\pi r^{2}}{\lambda}
$$

$r$ being the radius of the air-coupled transducer, and $\lambda$ being the wavelength of sound in air at frequency $f$. The values of $R_{0}$ are 72.5 mm for the transducer with a central frequency of 220 kHz and 45.4 mm for the transducer with central frequency of 310 kHz . Both values for $R_{0}$ are indeed surpassed by the 200 mm radius in our experiments.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-093_1270_1128_1181_392.jpg)

Figure 4-5 (a) Time waveform of a typical reflected wave of the 220 kHz transducer and (b) its frequency spectrum.

In general the exact normal direction to the scanned surface is a priori an unknown parameter and must first be determined by means of calibration on a flat and smooth surface on which the rods later be stacked. The flat surface on which the polar scan is performed is a 30 mm thick aluminum disk which represents actual conditions observed in the pasta fabrication process.

After calibration the polar scan on the periodic surface (Figure 4-6) is performed from -50 degrees (to the left side of the normal position of the horizontal surface) to +50 degrees (to the right side of the normal position of the horizontal surface). Symmetry of the scan range provides one Bragg angle of the same existing order on each side.

The main data processing process is to obtain the angular spectrograms of each polar scan from the angle-time domain waveforms directly obtained from the polar scans. This process is done through FFT using rectangular windows. Both the calibration of the normal position of the scanned surface and extraction of angle-frequency data for the purpose of acquiring periodicity of the periodic structures are based on these angular spectrograms.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-094_799_1034_1708_539.jpg)

Figure 4-6 Scan range to detect the backscattered beam at Bragg-angles.

### 4.4 Results and Discussion

Through a polar scan on the periodic structures composed of spaghetti rods Bragg scattering is investigated; Bragg angles and the corresponding frequencies are determined from the angular-spectrogram of the experimentally obtained signals. Accordingly, the periodicity of the tested structure is determined. The experiments are done both with a transducer of good quality (220 kHz) and with a transducer of poor quality (310 kHz). First, results obtained from the 220 kHz transducer are extensively explained and are further briefly compared with results from the 310 kHz poor quality transducer. When processing the measured data we noticed that the kind of stacking (see Figure 5-2) did not influence the measurements. This is due to the large acoustic impedance mismatch between dry pasta and air making most of the incident acoustic energy reflected back at the interface between air and the first layer of staking structure and therefore preventing the sound reflected from the deeper staking structure to have a significant influence on the measurements. Angular spectrograms in this paper are always normalized, i.e. the maximum visible amplitude is set to ‘1’ and all other amplitudes are given relatively. Since pattern recognition and determination is the main purpose of these spectrograms, the actual amplitude values are not important whence normalization is acceptable.

### 4.4.1 Calibration and Method for Data Extraction

A Fourier transform is performed on the back-reflected acoustic signals from the flat surface obtained using the 220 kHz air-coupled transducer. The resultant angular spectrogram is determined as shown in Figure 4-7. It can be observed from Figure 4-7 that an angle-frequency ‘fringe pattern’ and ‘high intensity’ area exist on the angular
spectrogram and that they are both symmetric with respect to a vertical centerline. Obviously this symmetrical centerline corresponds physically to the normal position of the scanned surface. In order to calibrate further measurements the offset corresponding to the exact position of the centerline must be determined. Hereby 2 procedures (Approach I and Approach II) of data analysis are outlined which are applied first to determine the offset and in subsequent sections to determine the Bragg angles. Although both procedures deliver practically the same result under favorable conditions, we will show later that for poor quality transducers one technique can replace the other when not utilizable.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-096_775_1381_1150_366.jpg)

Figure 4-7 Angular spectrogram of the polar scan on a flat surface obtained using the aircoupled transducer with central frequency of 220 kHz . The characteristics of the angular spectrogram used for data reading such as diminutive fringes and major fringe are shown.

Approach I scans the diminutive fringes and determines the coordinates of the highest amplitude spot in every fringe; calibration is then based on the fact that those spots lay exactly on the centerline. Approach II determines the geometrical center of the major fringe area; calibration is then also based on the fact that this spot coincides with the centerline.

When applied in subsequent sections to back-reflected sound on a periodic structure Approach I and Approach II are equally used to determine Bragg angle versus frequency pairs. Contrary to Approach II multiple spots are possibly considered in Approach I. Each spot is the center of a fringe. For each measurement, i.e. for each fringe, we take the spot with the maximum intensity as its center; then we give equal importance (weight) to every such found center when averaging over all fringes. For accuracy and to avoid human decision-making during any of the applied procedures we always measure as many fringe centers as possible when pursuing Approach I. The calibration process of the 220 kHz transducer enabled reading of 20 spots and the average value was considered to be the offset obtained from Approach I. We then decided to take the average of Approach I and Approach II as the actual offset of the transducer. Approach I resulted in an offset of 1.030 degrees, Approach II in 1.210 degrees, hence an offset of 1.120 was used.

### 4.4.2 Method to Extract Bragg Angles for Diffraction Frequencies

The determined offset is applied to all results for the 220kHz transducer. Fourier transformations are performed on the signals acquired from the polar scan on the periodic samples composed of rods of diameter 1.385 mm, 1.665 mm and 1.915 mm using the 220 kHz air-coupled transducer and the resultant angular spectrograms are obtained and respectively depicted in Figure 4-8 (a), (b) and (c). In each angular spectrogram the middle signal corresponds to the specular reflection from the periodic surface at the normal position and the other two signals correspond to the first backscattered beams at the Bragg angles. Because the same transducer is used in the same experimental setup and according to the same experimental procedure as during the calibration process the signals in the angular spectrograms shown in Figure 4-8 have the
same characteristics (or ‘fingerprint’) as the signals in the angular spectrogram shown in Figure 4-7, more in particular one can notice similar ‘diminutive fringe areas’ and similar ‘major fringes’. Extraction of Bragg angles is therefore done similarly using ‘Approach I’ and ‘Approach II’ on each of those patterns as was done during calibration as described in the previous section. For “Approach I” we extracted 15 spots, determined the corresponding rod diameter for each of the 15 Bragg angle versus Bragg frequency pairs and averaged the obtained values while keeping track of the standard deviation. For “Approach II” one point was determined based on the geometrical center of the major fringe and hence no statistical analysis was applicable to Approach II.

### 4.4.3 Periodicity Evaluation Using Approach I

The 15 pairs of Bragg angle-frequency values, as mentioned in the previous sections, for each periodic structure are obtained from Figure 4-8 and are depicted in Figure 4-9 while referring to the theoretically expected value (in solid line) based on the diameter measurement using a digital caliber, i.e. 1.385 mm (Sample 1), 1.665 mm (Sample 2) and 1.915 mm (Sample 3), and on Equation (4-5). It can be observed that the Bragg angle-frequency values obtained from the angular-spectrograms and their theoretical expectations are consistent which again shows that Approach I is reliable. For every determined Bragg angle versus frequency pair the corresponding rod diameter, calculated using Equation (4-5), is shown in Figure 4-10 for every sample. Again consistency is visible. Results are summarized for further comparison in Table 4-2.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-099_2131_1313_269_342.jpg)

Figure 4-8. Angular spectrogram of the polar scan on the periodic surface composed of cylindrical rods with average diameter of (a) 1.385 mm, (b) 1.655 mm and (3) 1.915mm obtained using an air-coupled transducer of central frequency of 220 kHz.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-100_686_1246_281_387.jpg)

Figure 4-9 Comparison of the Bragg angle-frequency values acquired in Approach I from their angular spectrograms and their theoretical expectations (bold line) for three sample periodic surfaces. For the frequency range of 210 to 225 kHz no Bragg angle-frequency values are available because of the existence of major fringes which blur the fringes.

### 4.4.4 Periodicity Evaluation Using Approach II

Table 4-2 presents a summary of the results obtained by Approach II in comparison with Approach I and with the direct measurement. It can be seen that the obtained results are consistent with the ones obtained by Approach I.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-100_688_1323_1746_351.jpg)

Figure 4-10 Diameters of the construction cylindrical rods obtained based on Bragg anglefrequency values acquired in Approach I for three sample periodic surfaces.

Table 4-2 Comparison of the periodicity measurements of three samples obtained in direct measurement, Approach I at 220 kHz and Approach II at 220 kHz. ‘SD/A’ refers to the ratio of the standard deviation to the mean. ‘Difference’ refers to the percentage difference between the mean diameter obtained from the angular spectrogram and that obtained with the direct measurement.
| Methods | Direct measurement | | | Approach I | | | Approach II | | |
| :— | :— | :— | :— | :— | :— | :— | :— | :— | :— |
| | Set 1 | Set 2 | Set 3 | Set 1 | Set 2 | Set 3 | Set 1 | Set 2 | Set 3 |
| Average [mm] | 1.385 | 1.665 | 1.915 | 1.381 | 1.634 | 1.898 | 1.361 | 1.649 | 1.928 |
| SD/A [%] | 1.30 | 1.23 | 1.08 | 0.67 | 0.87 | 0.79 | 0.46 | 0.41 | 0.69 |
| Difference [%] | 0.00 | 0.00 | 0.00 | -0.29 | -1.84 | -0.87 | -1.76 | -0.97 | 0.72 |

### 4.4.5 Comparison between Direct Measurements and Ultrasonic Evaluations

The average values of the periodicities obtained by two ultrasonic approaches, the corresponding ratio of the standard deviation (SD) to the mean (A) and the percentage difference from the direct measurements are also listed in Table 4-2.

It can be observed that (i) the ratios of standard deviation to the mean for all the three samples obtained in Approach I and II are less than 1% and that (ii) the differences between the average values of the rods obtained in Approach I and II and those obtained in direct measurements are less than 2%. Consequently it can be concluded that the periodicities obtained in Approach I and II are consistent and reliable.

### 4.4.6 Robustness Investigation of the Applied Method for the Poor Quality 310 kHz Transducer

Earlier it has already been indicated that the price and therefore the quality of the transducer may possibly have a significant impact on the reliability of the measurements. Irrespective of the actual frequency bandwidth of the transducer we consider the quality being related to the divergence of the beam and to the shape of the frequency spectrum; a
complicated spectrum may indeed result in patterns interfering with characteristics originating from the rods, which is a non-desirable phenomenon. The more Gaussianlike the spectrum and the less spreading of the beam, the higher the quality with respect to the experiments presented in this report. A careful investigation (not presented here) shows that for the 220 kHz transducer the divergence is 12 degrees, whereas the bandwidth is 11 kHz. For the 310 kHz transducer the divergence is 22 degrees, whereas the bandwidth is 40 kHz . Additionally the maximum intensity of the produced beam by the 310 kHz transducer is 6.24 times lower than for the 220 KHz transducer. Also the shape of the frequency spectrum of the 220 KHz transducer resembles much more a Gaussian function than that of the 310 kHz transducer. Clearly the 310 kHz transducer is therefore of much lower quality than the 220 kHz transducer. When for instance the experiment as presented in Figure 4-8 (1.915 mm rods) is done over with the poor quality 310 kHz transducer, the angular spectrogram obtained is shown in Figure 4-11.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-102_808_1479_1530_363.jpg)

Figure 4-11 Angular spectrogram of the polar scan on the periodic surface composed of cylindrical rods with average diameter of 1.915 mm obtained using a poor quality aircoupled transducer of central frequency of 310 kHz . A poor quality of the measured results is clear when compared to Figure 4-8 (c). Nevertheless it is possible to extract the diameter with relatively high accuracy.

Comparison with Figure 4-8 clearly shows that the results are of lower quality. Nevertheless it is possible to extract the diameter with high accuracy if the best method is applied to the most suitable Bragg diffraction order - so far we have only concentrated on the first Bragg diffraction order. Table 4-3 shows results obtained by the 310 kHz transducer using both Approach I and Approach II either on the first Bragg diffraction order or on the second Bragg diffraction order. It can be seen that good results can still be obtained despite the poor quality of the transducer if the most suitable method is used for the most suitable Bragg diffraction order. More precisely, we can see that Approach I works quite well (the results are consistent and relatively accurate) both on the first order and second order Bragg angles. However, overall the Approach II does not work that well since inconsistency and relatively larger errors are noticeable.

Table 4-3 Comparison of the periodicity measurements of three samples obtained from the first order and second order Bragg angles in Approach I and Approach II using the 310kHz transducer. ‘SD/A’ and ‘Difference’ are defined in Table 4-2.
| Methods | Approach I ( $1^{\text {st }}$ Order) | | | Approach I ( $2^{\text {nd }}$ Order) | | | Approach II ( $1^{\text {st }}$ Order) | | | Approach II ( $2^{\text {nd }}$ Order) | | |
| :— | :— | :— | :— | :— | :— | :— | :— | :— | :— | :— | :— | :— |
| | Set 1 | Set 2 | Set 3 | Set 1 | Set 2 | Set 3 | Set 1 | Set 2 | Set 3 | Set 1 | Set 2 | Set 3 |
| Average (mm) | 1.415 | 1.647 | 1.927 | 1.407 | 1.597 | 1.905 | 1.388 | 1.519 | 1.783 | 1.523 | 1.584 | 1.842 |
| SD/A [%] | 1.80 | 1.60 | 1.95 | 0.88 | 1.21 | 0.67 | 11.87 | 5.50 | 10.32 | 2.74 | 3.12 | 4.25 |
| Difference [%] | 2.17 | -1.08 | 0.63 | 1.59 | -4.08 | -0.52 | 0.22 | -8.77 | -6.89 | -8.53 | -4.86 | -3.81 |

### 4.5 Conclusions

Diffraction of ultrasonic waves in air from periodic structures is confirmed and Bragg angles have been detected in a polar scan using air-coupled transducers. The experimental results do not depend on the 2-dimensional stacking properties of rods and
are therefore only determined by the upper row of rods in the stack. The acquired timedomain polar scan signals are converted to frequency-domain signals and consequently angular-spectrograms, using the Fourier transformation. From the obtained angularspectrograms the periodicity and therefore the rod diameter is determined. Two measurement approaches have been presented that work equally well and with high accuracy and consistency for relatively high quality transducers, whereas for very low quality transducers it can be important to make a proper selection of the Bragg diffraction order when more than one order falls within the angular spectrogram.

Despite the fact that no expensive and very high quality transducers have been used for this research it turns out that accurate and robust results can be obtained. Considering the relevance of air-coupled ultrasonic investigations for the described industrial applications this study therefore promises wide industrial applications.

## RESUME DU CHAPTRE V

La caractérisation précise des dimensions caractéristiques d’une surface périodiquement ondulée en utilisant la technique d’imagerie par ultrasons est ici étudiée théoriquement et expérimentalement. Est egalement discutée la possibilité de caractériser avec précision les dimensions caractéristiques. La condition pour une caractérisation précise ainsi que le rapport quantitatif entre la précision et les paramètres de détermination sont indiqués. Les stratégies pour éviter les effets de diffraction suscitées par la nature périodique d’une surface ondulée sont également discutés. Les principales causes de mesures erronées sont théoriquement et expérimentalement discutés et illustrés. Une comparaison est faite entre les résultats présentés et les mesures optiques, révélant un accord acceptable. Ce travail expose de façon réaliste la capacité de la technique à ultrasons ˋa caractériser avec précision les dimensions latérales et verticales caractéristiques de surfaces ondulées . Tant les principes généraux développés en théorie que les techniques pratiques proposée peuvent servir de lignes directrices utiles à leurs pairs.

## CHAPTER V

## ULTRASONIC GEOMETTRICAL CHARACTERIZATION OF PERIODICALLY CORRUGATED SURFACES

### 5.1 Introduction

Periodically corrugated structures are ubiquitous; they appear in everyday life as well as in sophisticated technological applications ranging from large-scale architectural structures [1-5] to small-scale photonic or phononic crystals [6]. Generally the geometry of the corrugated structures is crucial for the designed functionality and hence nondestructive characterization is of general interest during the design as well as during the manufacturing process.

Ultrasound is generally accepted as a useful nondestructive characterization tool for surface integrity and quality determination [7-9] and has certain advantages when compared to optical microscopy such as its capability to determine not only the lateral dimensions of features, for instance the width of defects, but also features perpendicular to it, for instance the depth or height of defects. For this reason a thorough investigation is envisaged in this work on the actual ability of ultrasound to characterize surface dimensions and its limitations.

A long history preceding the current work can be found in the literature on interaction of sound with corrugated structures [10-15]. A considerable range of numerical techniques exists to simulate the interaction of sound with a periodic corrugation [12, 13, 16, 17]. Determination of the geometric properties is normally done indirectly by comparison between the experimental and the numerical diffraction spectra. The results are, of course, strongly biased by the assumptions and idealizations made in the applied theoretical models; hence results are normally far off reality. In addition each
theoretical model has its own inherent limitations concerning the range of applicability and will produce unrealistic results when used outside that range [18-21].

From the experimental point of view limitations are of course imposed by the available scanning devices and transducers and by physical acoustic effects such as diffraction of sound caused by the considered structure. Generally spoken one may conclude that the existing studies show that the periodicity of a corrugated structure can be rather accurately determined, even with limitations imposed by the indirect determination based on theoretical models or by the presence of diffraction effects during experiments. The real challenge however is an accurate determination of features at the sub-periodicity level, such as the profile (shape and depth) of the grooves.

Acoustic microscopy could be considered for that purpose and will be successful for small depths (i.e. not deeper than the very short focal length of the acoustic objective) [22-24], but for the corrugation with large vertical dimension this technique will lose its accuracy due to its very short focal zone [25]. In addition, the technique is too slow to scan extensive corrugated structures and is not time efficient in terms of signal processing. As a matter of fact acoustic microscopy is simply too accurate for this purpose and could cynically be compared to using an optical microscope to read a newspaper. When lower frequencies are used instead, scanning a surface is a lot faster without loss of capacity to reveal features of the order of magnitude of the applied wavelengths and furthermore faster signal processing techniques such as time of flight or amplitude determination. However, as the used wavelengths approach the dimensions of the corrugated structure one enters shark-infested waters because disruptive physical effects may occur such as diffraction effects, which should either be fully understood and mastered, or be avoided.

In what follows we theoretically investigate the principles and requirements that are helpful in choosing proper testing equipment and in avoiding diffraction effects. An additional focus of the investigation is on the effects of different factors, such as transducer beam properties and sampling intervals, influencing the characterization accuracy.

### 5.2 Samples and Experimental Setup

### 5.2.1 Samples

Three brass blocks (Samples I, II and III) are investigated experimentally. Each sample has a geometric profile of periodic corrugation on its top surface, while the bottom surface is smooth. The thickness of the brass blocks is sufficiently large to enable windowing of any signals reflected off the top surface only. Optical microscopic images of the top and side surfaces of each sample are provided in Figure 5-1. It can be readily seen that each top surface is partially flat and partially corrugated. The corrugation can be seen as a subsequent combination of surface areas at two different heights. To ease explanations further in this paper the areas at the same height as the flat surface area are called plateaus, whereas those forming the lower parts of the grooves are called valleys. Note that the plateaus are polished before machining the grooves and are therefore smooth, while the valleys are more roughish as a result of the machining process. This can be confirmed first by examining the images in Figure 5-1, which will be further confirmed in Section 5.4.1.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-109_820_1140_248_459.jpg)

Figure 5-1 Top and side views of the three corrugated brass samples: (a) and (b) are Sample I; (b) and (c) are Sample II; (e) and (f) are Sample III.

The corrugations as studied here can be primarily characterized by four geometric parameters: periodicity $(\Lambda)$, plateau width $\left(\Lambda_{\mathrm{P}}\right)$, valley width $\left(\Lambda_{\mathrm{V}}\right)$, and corrugation height (H), i.e. the height difference between plateaus and valleys. From the side views of the three samples (Figure 5-1 (b), (d) and (f)) it can be observed that the transition from plateaus to valleys is not exactly vertical, but inclined. These inclined surfaces scatter sound waves. These scattered waves barely contribute to the specular reflection from both the plateaus and the valleys, but as experiments expose in time domain they are more disposed towards sound reflected from the valley than from the plateau. These facts and the small horizontal dimensions of these inclinations, allow us to reasonably add their horizontal dimensions to those of the valleys $\left(\Lambda_{\mathrm{V}}\right)$. Given the aforementioned considerations the following relationship holds:

$$
\Lambda=\Lambda_{P}+\Lambda_{V}
$$

For further use in this paper we define the ratio of plateau width to corrugation periodicity as

$$
k_{P}=\frac{\Lambda_{p}}{\Lambda}
$$

A direct measurement of 10 corrugations of each sample is performed on optic microscopic cross sectional (side) images. The average value (A) of the four geometric parameters of corrugation, together with their respective ratio of standard deviation to average value (SD/A), are listed in Table 5-1. By comparing the ratio of standard deviation to average value of each geometric parameter of all the three samples we can see that the corrugations of Sample II have better geometric consistency, hence a better corrugation quality, than the other two samples.

For the convenience of notation and explanation two directions are introduced: (i) ‘scan axis’, i.e. the direction perpendicular to the corrugation grooves; and (ii) ‘index axis’, i.e. the direction parallel to the corrugation grooves. In addition, the total thickness of Sample III is observed as not being uniform in the direct measurement along the direction of scan axis, and this will be confirmed later in Section 5.4.2.

Table 5-1 Corrugation characteristic dimensions of the samples: the average value (A) and their respective ratio of standard deviation to average value (SD/A).
| Sample | $\Lambda$ | | $\Lambda_{\mathrm{P}}$ | | $\Lambda_{\mathrm{V}}$ | | H | |
| :— | :— | :— | :— | :— | :— | :— | :— | :— |
| | A ( $\mu \mathrm{m}$ ) | SD/A (%) | A ( $\mu \mathrm{m}$ ) | SD/A (%) | A ( $\mu \mathrm{m}$ ) | SD/A (%) | A ( $\mu \mathrm{m}$ ) | SD/A (%) |
| I | 185 | 4.5 | 75 | 6.7 | 110 | 4.3 | 25 | 7.7 |
| II | 309 | 0.9 | 111 | 2.4 | 198 | 2.0 | 80 | 3.8 |
| III | 515 | 2.2 | 121 | 7.0 | 395 | 5.9 | 238 | 5.2 |

### 5.2.2 Experimental Setup

The ultrasonic scanner used in this experiment is a customer-designed high frequency scanner fabricated by ‘Inspection Technology Europe BV’. The transducer chosen for the scan is a ‘Valpey Fisher’ focused immersion transducer with parameters provided by the manufacturer: central frequency (f) of 100 MHz, spherical focal length $(F)$ of 12.7
mm (0.5 inch) and transducer diameter (D) of 2.54 mm (0.1 inch). All the experimental data are acquired using ‘Winspect’ software and are further processed using ‘Matlab’. For correctness the transducer parameters provided by the manufacturer were not used directly, but measurements have been taken instead. The measurement of the spectrum of an echo reflected from the smooth area of the samples reveals a -6 dB (compared with the maximum amplitude value) frequency coverage of 22 MHz to 72 MHz and hence a -6 dB bandwidth of 50 MHz . The measured central frequency turned out to be 45 MHz .

An experimental characterization of the geometrical properties of the acoustic field of the transducer was preformed in pulse-echo mode using a cylindrical steel reflector. This characterization confirmed the values of the focal length and the beam diameter provided by the manufacturer, and also provided a focal zone (beam waste) of about 2 mm and a -6 dB focal diameter of the transducer beam of $209 \mu \mathrm{~m}$, which is also close to the expected value of $201 \mu \mathrm{~m}$ obtained from the following commonly used relationship:

$$
B D(-6 d B)=1.22 F c / f D
$$

with $B D$ the focal diameter of the transducer beam, $F$ the spherical focal length, $c$ the sound velocity in water (1480 m/s) measured in our laboratory, $f$ the central frequency and $D$ the transducer diameter. These beam parameters have a good agreement with the theory developed by H. T. O’Nail [26].

The scans are performed in water under pulse-echo mode for a rectangular scanning area of 12 mm (scan axis) by 4 mm (index axis). In order to obtain the highest resolution the transducer can possibly offer the time domain window for acquiring the reflections is set between $16.30 \mu \mathrm{~s}$ and 17.10 us because their corresponding range of $12.06 \mu \mathrm{~m}$ to $12.65 \mu \mathrm{~m}$ is exactly in the focal zone of the focused beam. The spatial resolution of the
scan for both axes is $20 \mu \mathrm{~m}$ and the temporal resolution is $0.002 \mu \mathrm{~s}$, which corresponds to a sampling frequency of 500 MHz .

### 5.3 Dominating Factors of Characterization Quality

High quality characterization of corrugated surfaces requires a proper control of many factors such as the characteristics of the ultrasonic beam as well as the sampling characteristics.

### 5.3.1 Spectral Properties of the Transducer Beam

In this section the effects of frequency related properties of an ultrasonic beam on corrugation characterization are discussed.

### 5.3.1.1 Bandwidth and spatial resolution

Although the spectra of the ultrasonic pulses used in experiments like ours are never exactly Gaussian per se, still they are to a good approximation Gaussian-like in most cases. We therefore apply knowledge based on Gaussian pulses to the investigate corrugation geometry in a meaningful manner. According to the Fourier transform theorem concerning real signal frequency translation [27] a spectrum shifted by a value $f_{\text {shift }}$ corresponds to the original time domain signal multiplied by a harmonic function in time, and so the only influence of $f_{\text {shift }}$ is the phase change, not the amplitude change, of the original time domain signal. Therefore, the time domain duration of an incident pulse ( $\tau$ ) is only a function of the bandwidth of a transducer beam ( $\beta$ ) and is not affected by the central frequency of the transducer. This relationship is expressed in Equation (5-4).

$$
\tau \propto 1 / \beta
$$

This means that a pulsed beam having a larger spectral bandwidth can produce a shorter time domain pulse. As is well-known in ultrasonics the time domain length of a pulse determines its ability to distinguish between two adjacent targets along the direction of wave propagation, i.e. its spatial resolution. Given the pulse duration $(\tau)$ and sound speed in the medium ( $c$ ) the spatial resolution of a pulse ( $R$ ) can be obtain from Equation (5-5).

$$
R=\tau c / 2
$$

Considering the spatial resolution $(R)$ relative to the corrugation height $(H)$, the reflections from corrugation surfaces can be categorized into two cases:

1. If $R>H$, the reflections from the plateau and valley surfaces overlap as shown in Figure 5-2 (a) and this makes it impossible to correctly characterize the two individual reflection surfaces.
2. If $R \leq H$, the reflections from the plateau and valley surfaces can be properly separated from each other in the time domain waveform as shown in Figure 5-2 (b) and (c). The disconnection of these two reflected echoes enables the characterization of their originating surfaces.

Therefore, the relationship between spatial resolution and corrugation height actually governs the possibility of characterization of a corrugation. For this study the pulse has a length of $0.04 \mu \mathrm{~s}$ and a corresponding spatial resolution of $59.2 \mu \mathrm{~m}$. Comparing this value to the corrugation heights of the three samples listed in Table 1 it can be concluded that Samples II and III can be reliably characterized, however Sample I cannot. Thus, in this work only the experimental results of Sample II and III are reported.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-114_972_1516_269_303.jpg)

Figure 5-2 Reflections from the corrugated surfaces of (a) Sample I, (b) Sample II and (c) Sample III.

### 5.3.1.2 Central frequency and wavelength

Whereas the previous section dealt with the bandwidth, duration of a pulse and in-depth resolution, the current section deals with the central frequency as this is not only a determining factor in the detection resolution, but equally important in the possible occurrence of diffraction.

With high frequency comes smaller wavelength. It is well known that small wavelengths are more sensitive to small surface defects than large wavelengths and they therefore lead to higher detection resolution of the surface geometry. For the purpose of obtaining higher detection resolution the transducers with high central frequency are preferred in this work. Another issue concerning wavelength is the effects of diffraction on the geometric characterization because the tested corrugations can possibly act as a diffraction grating.

The general rigorous condition for acoustic diffraction is that the wavelength of sound is in the same order of the periodicity of the grating [18-20]. In the current work the range of wavelengths of the incident pulse is from $21 \mu \mathrm{~m}$ to $67 \mu \mathrm{~m}$ corresponding to a frequency range of 22 MHz to 72 MHz . As can be verified this range does not cover the periodicities of our samples ( $185 \mu \mathrm{~m}$ for Sample I, $309 \mu \mathrm{~m}$ for Sample II and $515 \mu \mathrm{~m}$ for Sample III) and hence diffraction has little effect on the accuracy of geometric characterization of the envisaged corrugations. In this respect one can clearly see that in order to avoid the effects caused by diffraction on the corrugated structure characterization, once again high frequency transducers are preferred.

### 5.3.2 Ultrasonic Beam Diameter

In this study the ultrasonic pulse-echo mode is applied and the characterization of the corrugation geometry is therefore based on the properties of echoes reflected from corrugation surfaces. The basic requirement for accurate characterization of a surface corrugation using this testing mode is that the echo properties should be able to correctly show the alternating plateaus and valleys on which the center of the transducer beam is positioned.

Three cases exist: (a) only a reflection from the plateau surface occurs, (b) only a reflection from the valley surface occurs, and (c) both reflections occur simultaneously due to a partial coverage of the beam on plateau and valley surfaces. Clearly the first two cases resolve the valleys from the plateaus. For the third case the resolution will depend on the relative energy of the two received echoes. As will be described below, the echo with higher energy (and therefore also a higher amplitude) determines the section (valley or plateau) scanned at that location. The third case (c) is prevalent and requires the necessary caution and understanding.

In the third case (c) a valley or a plateau just underneath the center of the beam will cause a predominant echo reflected from that surface area. As the beam moves to the adjacent position during a scan the result will be more ambiguous and requires a preliminary study to allow understanding of this phenomenon and to determine how wide the incident ultrasonic beam can be to enable accurate characterization. For a theoretical investigation we assume (i) that a beam has a uniform intensity distribution throughout its cross section, which is reasonable for an actual beam within its focal zone and, for simplicity, (ii) that the plateau and valley surfaces have equal reflective properties. Under these two assumptions the reflected energy in the two echoes, is proportional to its respective reflection area that is directly related to the beam diameter for a given corrugation.

Figure 5-3 illustrates the effects of the beam diameter on the reflection energy. The results shown are obtained from the simulation on a corrugation with a ratio of plateau width to periodicity $\left(k_{P}\right)$ of $35.9 \%$ (i.e. Sample II). We define the minimum corrugation geometry (MCG) as

$$
M C G=\min \left\{\Lambda_{P}, \Lambda_{V}\right\}
$$

In the example of Figure 5-3 MCG is equal to $\Lambda_{P}$. Four beam diameters as shown in Figure 5-3 (a) are investigated and they represent four different cases (from left to right): (i) a beam diameter $D<M C G$, (ii) $D=M C G$, (iii) $D$ slightly smaller than $\Lambda$ and (iv) $D=\Lambda$. The normalized energy, i.e. the ratio of the energy reflected from individual surface to the total reflected energy, of the two types of echoes for the four cases are shown in Figure 5-3 (b) to (e).

We formulate the following conditions without which an accurate characterization fails. When the incident beam is centered above a valley, the reflection coming from the
valley must dominate. Similarly when the incident beam is centered above a plateau then the reflection coming from the plateau must dominate. Additionally when a beam is centered at the transition from valley to plateau, both reflections must equally manifest themselves. Whether or not these conditions are met depends on the beam diameter for a given corrugation. Consequently the beam radius must not be larger than the smallest of the plateau width $\left(\Lambda_{\mathrm{P}}\right)$ and the valley width $\left(\Lambda_{\mathrm{V}}\right)$ as summarized in Equation (5-7 a); similarly the beam diameter must not be larger than two times the smallest of the plateau width $\left(\Lambda_{\mathrm{P}}\right)$ and the valley width $\left(\Lambda_{\mathrm{V}}\right)$ as shown in Equation (5-7 b).

$$
R \leq \min \left\{\Lambda_{P}, \Lambda_{V}\right\}
$$

or

$$
D \leq 2 \min \left\{\Lambda_{P}, \Lambda_{V}\right\}
$$

The cases shown in Figure 5-3 (b) and (c) satisfy the condition stated in Equation (5-7) and it can be observed that the normalized energies reflected from both corrugation surfaces dominate alternatingly, in a scan along the scan axis, at their respective intervals and that at the transition between valley and plateau their values are equal, namely 0.5. Even in Figure 5-3(d) the alternating dominancy of the two reflection energies during a scan can be observed but the difference is the positions where they alternate dominancy. More precisely these position do no longer coincide with the transition points but are rather located on the plateaus. The reason is that the beam diameter does not satisfy the condition described by Equation (5-7) and therefore a characterization error emerges. In this work the characterization error is defined as the difference between the measurement of either plateau width or valley width and the real value. A positive error means the measurement is larger than the real value, and a negative error means the measurement

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-118_2218_1184_253_438.jpg)

Figure 5-3 Effects of beam diameter on the reflected echo energy. Image (a) is the schematics of the periodic corrugations for the simulation and the cross sections of four

beams with different diameters. The lighter area is plateau and the darker area is valley. The value of $\mathbf{k}_{\mathbf{P}}$ is $\mathbf{3 5 . 9 \%}$ (Sample II). Image (b) to (e) show the normalized energy levels of plateau reflection, valley reflection and ideal plateau reflection for the four cases shown in (a) from left to right respectively. The beam diameter is $\mathbf{0 . 8} \boldsymbol{\Lambda}_{\mathrm{P}}$ or $\mathbf{0 . 2 8 7} \boldsymbol{\Lambda}$ for (b), $\mathbf{2} \boldsymbol{\Lambda}_{\mathrm{P}}$ or $\mathbf{0 . 7 1 8} \boldsymbol{\Lambda}$ for (c), $\mathbf{2 . 4} \boldsymbol{\Lambda}_{\mathbf{P}}$ or $\mathbf{0 . 8 6 2} \boldsymbol{\Lambda}$ for (d), and $\boldsymbol{\Lambda}$ for (e).
is smaller. As we further violate Equation (5-7), i.e. the case of Figure 5-3 (e), the energy level oscillation can still be observed, but there is no alternation anymore visible in dominance between the two reflections. As a further demonstration we take again the example of a $k_{P}$ value of $35.9 \%$. Figure 5-4 depicts the relative error of plateau width measurements as a function of the beam diameter when the beam diameter is smaller than the corrugation period $\Lambda$.

It can be seen in Figure 5-4 that the four cases as described in Figure 5-3 can be identified and that the cases (b) and (c) produce no error whereas case (d) produces an error which further increases as beam diameter increases and case (e) is totally erroneous. The general trend is always that 3 error regimes exist for any given corrugation. Relatively small beam diameters produce no error, larger beam diameters result in errors and the error values appear to saturate above a given diameter. In the saturation regime it is impossible to obtain other corrugation characteristic dimensions except for the periodicity itself of the corrugation. Two other observations can also be made.

1. For a given corrugation, the plateau width error $\left(\mathrm{E}_{\mathrm{P}}\right)$ is equal to the valley width error $\left(\mathrm{E}_{\mathrm{V}}\right)$, but with opposite signs. In other words
    
    $$
    E_{P}+E_{V}=0
    $$
    
2. The errors $\mathrm{E}_{\mathrm{P}}$ and $\mathrm{E}_{\mathrm{V}}$ as a function of $k_{P}$ show the following characteristics:
    
    $$
    E_{P}\left(k_{P}\right)+E_{P}\left(1-k_{P}\right)=E_{V}\left(k_{P}\right)+E_{V}\left(1-k_{P}\right)=0
    $$
    

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-120_765_1300_482_411.jpg)

Figure 5-4 Effects of beam diameter on characterization accuracy of plateau width

$\boldsymbol{\Lambda}_{\mathbf{P}}$

for five corrugations with different

$\boldsymbol{k}_{\boldsymbol{P}}$

. In this study Sample I has a

$\boldsymbol{k}_{\boldsymbol{P}}$

value of

$\mathbf{4 0 . 5 \%}$

, Sample II 35.9% and Sample III 23.2%.

The above discussions and statements cover an idealized situation as mentioned at the beginning of Section 5.3.2, and will accompany deviations in real life situations. Imagine the situation, as in our experiments when, as mentioned in Section 5.2.1, the plateau surface is smoother than the valley surface. The latter will clearly have lower reflectivity than the former. What is the effect of this difference? Well, when Figure 5-3 is re-examined taking into account lower reflectivity at the valley surfaces, the appearance of errors in positioning the transition area between valley and plateau will appear sooner with increasing beam diameter compared with the case where plateau and valley have equal reflectivity.

By applying the condition for accurate characterization stated in Equation (5-7) to the samples investigated in this work, it can be concluded that Samples II and III are being able to be accurately characterized, while Sample I is not. Considering the different
reflectivity of the plateau and valley surfaces we may assume that the experimental measurements of plateau width of Sample II and III will be larger than the real values. This assumption will be further examined in Section 5-4.

It is necessary to note that Equation (5-7) suggests the beam diameter should be smaller than one corrugation periodicity for accurately characterization. If so, we are dealing with a beam interacting with essentially one groove and not a corrugated surface. Hence diffraction will not influence the ability for accurate characterization of the corrugation geometry.

### 5.3.3 Spatial and Temporal Sampling Intervals

Because the investigated samples are periodical in nature, it is not uncommon to make a link with Nyquist’s theorem. Indeed a periodic structure results in a spectral signature when being looked at in the framework of signal analysis and Fourier transforms. Definitely Nyquist’s theorem applied here states that one must take twice the number of samples per meter as the highest spatial frequency in the Fourier transform of the mathematical function describing the structure. Only then can the structure be completely reproduced by means of a summation of orthogonal functions. Because a priori we have no idea of the actual function describing the periodic structure, we don’t know how many samples should be taken. Furthermore we have to deal with limitations governed by the used equipment. We hence apply the brute force approach and aim for the highest possible accuracy allowed by our equipment. For this study, the interval between two samples is $20 \mu \mathrm{~m}$ along the scan axis and along the index axis.

We apply the same brute force approach in time domain and take a sample rate of 500 MHz. It certainly obeys Nyquist’s theorem and the extra samples do not seem to cause significant signal processing delays. The applied sample rate means a temporal
interval between two samples of $0.002 \mu \mathrm{~s}$ which corresponds to a spatial (in depth) resolution of $3 \mu \mathrm{~m}$ in water.

### 5.3.4 Data Processing Methods

The choice of data processing methods depends on both the purpose and requirement of the experimental investigation and the properties of the waveform experimentally obtained. The purpose of the current research is to accurately determine the characteristic dimensions of the corrugation. As discussed in Section 5.3.2 the measurement is based on the relative energy of the plateau and valley reflections, which is of course directly determined by the relative amplitude. Therefore, practically, we use the amplitude and the time-of-flight (TOF) of the reflections to obtain the corrugation geometry.

In this work the difference between the maximum amplitude of the plateau reflection and that of the valley reflection are obtained for imaging the whole scanned area. The time of flight (TOF) of the peak with maximum amplitude is also used for imaging the corrugations. Theoretically, these two techniques are supposed to give the same results because they are based on the same reflections and this expectation will be confirmed in Section 5.4.1 when comparing results obtained by both techniques. Both techniques are equally capable of characterizing the lateral geometrical properties of corrugated surfaces, but they differ from each other in two aspects. The first difference is that the technique using amplitude can better characterize the small surface defects because amplitude is more sensitive to the energy loss caused by surface defects than TOF. The second difference is that the technique using TOF is capable of characterizing the vertical geometry, i.e. the corrugation height, by converting the TOF to distance in the direction of wave propagation given the sound velocity in the medium. All these are described in further detail in the next section.

### 5.4 Experimental Results and Discussions

### 5.4.1 Characterization of the Lateral Corrugation Geometry

The images of corrugation surface of Sample II and III obtained from the ultrasonic scans are shown in Figure 5-5 and Figure 5-6 respectively. For the purpose of comparison the image obtained with the technique using amplitude and the image obtained with the technique using TOF are shown together for each sample. The quantitative evaluation of the corrugation geometry based on the images indicates that the two techniques give the same results for both samples as predicted in Section 5.3.4. The statistical results of the lateral corrugation dimensions, the average (A) and the ratio of standard deviation to average (SD/A) are obtained based on 25 readings for Sample II and 15 readings for Sample III and they are listed in Table 5-2.

It is worth noting that amplitude have higher sensitivity to the surface defect including roughness than TOF and the images obtained with the technique using amplitude are expected to give us more details about the surface quality of the samples. In Section 5.2.1 it is mentioned that the plateau surfaces are relatively smoother than the valley surfaces for our samples, and these are confirmed by the observation from Figure 5-5 (a) and Figure 5-6 (a) that the color of the plateau surfaces are more uniform than the color of the valley surfaces. In addition, the color non-uniformity in the flat surface area of Sample III shown in Figure 5-6 (a) confirms the physical non-uniformity of this surface area shown in the optical image of Figure 5-1 (c).

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-124_957_1417_250_315.jpg)

Figure 5-5 The images characterizing Sample II based on (a) the difference between the maximum amplitude of the plateau reflection and that of the valley reflection and (b) the TOFs to the peaks with maximum amplitude.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-124_888_1354_1540_349.jpg)

Figure 5-6 The images characterizing Sample III based on (a) the difference between the maximum amplitude of the plateau reflection and that of the valley reflection and (b) the TOFs to the peaks with maximum amplitude.

### 5.4.2 Characterization of the Vertical Corrugation Geometry

As discussed in Section 5.3.4 the technique using TOF is capable for characterizing the vertical geometry of corrugation and this vertical characterization is shown in Figure 5-7 for both samples. The statistical results of the corrugation height obtained based on 25 readings for Sample II and 15 readings for Sample III are also listed in Table 5-2.

In addition, from Figure 5-7 (b) it can be observed that the upper surfaces of Sample III, i.e. its flat area and plateau surface, are obviously not horizontal. This observation confirms the physical measurement mentioned in Section 5.2.1.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-125_859_1330_1015_368.jpg)

Figure 5-7 The distance between the transducer surface and the scanned surface at the index position of 2 mm obtained based on the TOFs to the peaks with maximum amplitude for (a) Sample II and (b) Sample III.

Table 5-2 Corrugation characteristic dimensions obtained from the ultrasonic images: average value (A) and the ratio of standard deviation to average value (SD/A).
| Sample | $\Lambda$ | | $\Lambda_{\mathrm{P}}$ | | $\Lambda_{\mathrm{V}}$ | | H | |
| :— | :— | :— | :— | :— | :— | :— | :— | :— |
| | A ( $\mu \mathrm{m}$ ) | SD/A (%) | A ( $\mu \mathrm{m}$ ) | SD/A (%) | A ( $\mu \mathrm{m}$ ) | SD/A (%) | A ( $\mu \mathrm{m}$ ) | SD/A (%) |
| II | 304 | 5.5 | 121 | 14.4 | 179 | 10.5 | 94* | 0.1* |
| III | 508 | 4.7 | 140 | 27.5 | 368 | 12.3 | 253* | 1.5* |

[2](about:blank#fn2)
### 5.4.3 Comparison of the Results Obtained Using Different Techniques

The average values of the corrugation characteristic dimensions obtained from the optical microscopic images and ultrasonic images are compared in Figure 5-8, and their difference and the ratio of the difference to the corrugation periodicity are listed in Table 5-3.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-126_885_1484_751_332.jpg)

Figure 5-8 Comparison of the average values of the measurements for Sample II and III obtained with optical microscopic technique and the ultrasonic techniques using amplitude and TOF.

Table 5-3 Difference of the corrugation characteristic dimensions obtained using ultrasonic techniques and those obtained using optical technique (E) and the percentage ratio of the difference to the periodicity $(\mathrm{E} / \Lambda)$.
| Sample | $\Lambda$ | | $\Lambda_{\mathrm{P}}$ | | $\Lambda_{\mathrm{V}}$ | | H |
| :— | :— | :— | :— | :— | :— | :— | :— |
| | E ( $\mu \mathrm{m}$ ) | $\mathrm{E} / \Lambda$ (%) | E ( $\mu \mathrm{m}$ ) | $\mathrm{E} / \Lambda$ (%) | E ( $\mu \mathrm{m}$ ) | $\mathrm{E} / \Lambda$ (%) | E ( $\mu \mathrm{m}$ ) |
| II | -5 | -1.6 | 11 | 3.6 | -19 | -6.1 | 14 |
| III | -7 | -1.4 | 19 | 3.7 | -27 | -5.2 | 15 |

It can be readily seen from Figure 5-8 that the measurements of Sample II and III have the same changing tendency: the ultrasonic measurements of periodicity, plateau width are smaller than the optical ones, while the ultrasonic measurements of valley width and corrugation height are larger than the optical ones. This observation suggests that the source causing the difference is a systematic one and this conclusion is supported by the fact that the percentage ratio of the difference to the periodicity $(\mathrm{E} / \Lambda)$ of the two samples listed in Table 5-3 are very close to each other.

According to the discussion in Section 5-3 the main possible cause of the difference between ultrasonic and optical measurements for lateral corrugation dimensions are the relative size of beam diameter and lateral corrugation dimensions, spatial sampling interval and temporal sampling interval. Theoretically, the maximum difference between the measurements and the real values caused by spatial and temporal sampling are $20 \mu \mathrm{~m}$ and $3 \mu \mathrm{~m}$ respectively. These values make the difference of periodicity, plateau width and valley width listed in Table 5-3 acceptable assuming the optical measurements are closer to the real values.

In this study the condition for accurate characterization of corrugation geometry given in Equation (5-7) suggests no error for the ultrasonic measurements of the lateral corrugation geometry of the two samples. But as discussed in Section 5.3.2 considering the different reflectivity of the plateau and valley surfaces caused by their different roughness the measurement of plateau width are predicted to be smaller than the real value, while the measurement of valley width should be larger. This prediction is confirmed by observation of Figure 5-8 and by the data listed in Table 5-3 if assuming the optical measurements are more close to the real values.

As to the difference of the measurement of corrugation height in Table 5-3 the reason why the optical measurement is systematically lower is probably due to the technical
limitation of the optical technique. As a matter of fact the optical measurement can only be performed on the side of the corrugation while the corrugation height inside the corrugation is larger than that of the side, which suggests the probable error in the optical measurement of the height and the probable correctness of the ultrasonic measurement of the height.

### 5.5 Conclusions

In this work accurate characterization of the geometric properties of periodically corrugated surfaces using ultrasonic techniques is investigated both theoretically and experimentally. In the theoretical investigation the dominating factors for a high quality characterization are discussed in terms of their effects on the possibility and accuracy of characterization. As a summary, the important conclusions of the theoretical investigation are listed below:

1. The possibility of geometric characterization of a corrugated surface using the proposed ultrasonic methods is determined by the relationship between the corrugation height and the spatial resolution of the transducer beam.
2. The theoretical condition for accurate characterization of corrugation geometry is that the beam radius should be smaller than the smallest of the corrugation characteristic dimensions.
3. A higher frequency transducer is highly recommended to increase the detection sensitivity, and hence the detection resolution.
4. The main sources of possible measurement error are the difference of surface roughness of plateaus and valleys, causing a different reflectivity, and the spatial sampling interval.

The experimental work illustrates the effectiveness of the principles discussed in the theoretical part and further analyzes the possible reasons for the difference between ultrasonic measurements and optical measurements of all the characteristic dimensions of corrugation. A comparison between the ultrasonic technique and the optical technique reveals similar results with small differences that are connected to the difference of reflectivity of the valleys compared with the plateaus. Furthermore it has been discussed that acoustic microscopy for imaging corrugated surfaces is not per se beneficial and would certainly limit scanning speed and investigation range, whereas frequencies that are too low may cause diffraction and would make imaging of a corrugation hardly possible. The intermediate frequencies as presented here are sufficiently capable of imaging the main corrugation properties such as corrugation height and the width of the corrugation valleys and plateaus without compromising speed and scanning range. This work proves that ultrasonic techniques are capable of accurately characterizing the lateral and vertical dimensions of corrugated surfaces.

## RESUME DU CHAPTRE VI

Ce travail étudie l’impact des défauts de caractérisation dans le cas oú le bruit de haut niveau est inévitable en raison du système d’acquisition de données impliqué. Une technique d’extraction d’urgignal reposants ur l’analyse spectrale du signal fenêtré est propose. Les images obtenues par C-scan sont comparées à celles obtenues en utilisant des techniques d’extraction de propriétés de signaux conventionnelles. Il est prouvé que l’intérieur de la plage de sensibilité de fréquence de la technique proposée est non seulement capable de caractériser les défauts, mais s’avère prometteuse quant à l’estimation des dimensions de défaut.

## CHAPTER VI  SPECTRAL ANALYSIS OF THE IMPACT DEFECTS IN COMPOSITE PLATES

### 6.1 Introduction

Composite plate materials are widely used in almost all branches of modern industries and everyday life. Detection and characterization of the impact defects of the composite plates are of great interest in quality control during manufacturing process and health monitoring during practical service and application [1]. Among a variety of nondestructive methods immersion (water-coupled) ultrasonic testing is a good choice due to its high reliability, efficiency and low cost [2]. In this work the immersion ultrasonic technique is applied to detect the impact damage of a carbon/epoxy plate.

The difficulties in interpreting and understanding ultrasonic signals are commonly recognized and some of the difficulties are caused by the imperfection of data acquisition system such as low quality transducers, etc., which distorts or degrades the acquired signals [3]. A lot of effort has been devoted to signal processing for composite defect characterization. Tarantola & Valette [3] and Bochud et al. [4] tried the inverse problem approach; Sin & Chen [5] developed the spectral extrapolation; and Wooh & Wei [6] developed homomorphic deconvolution by computation of cepstrum, ect. However, there is no universal methods applicable to all the situations encountered in signal processing for impact defect characterization and in most cases an individual situation has to be treated specifically. In this study we deal with the case in which unavoidable high-level noise caused by the data acquisition system is involved. A frequency domain based signal property extraction method is proposed for C-scan imaging of the composite plate.

The experimental work and signal processing are discussed in details in the following parts of this section.

### 6.2 Experiments

### 6.2.1 Specimen

The specimen tested in this work is a carbon/epoxy plate with the dimensions of 120 mm long, 120 mm wide and 2.35 mm thick. The damages were generated by applying controlled free-fall impact energy: an impactor of 50 g with two blades of 0.385 mm wide hitting the specimen at a speed of 9.35 m/s. After being impacted the specimen was covered with a thin layer of white pain concealing surface defects. The images of the scanned area of the specimen obtained by optical imaging and ultrasonic imaging techniques are shown in Figure 6-1. In the optical image of the composite plate sample shown in Figure 6-1 (a) the horizontal line pointed by an arrow is the approximate location where the impact and the corresponding defect were made, and the red square is the scanning area for defect testing. The ultrasonic image of the sample shown in Figure 6-2 is obtained from a pulse-echo scan using a 30 MHz immersion transducer. Compared with the optical image the surface roughness and texture of the sample is much easier to be observed from this ultrasonic image. The horizontal line in the ultrasonic image corresponds to the one in optical image; the dents show the roughness of the surface, i.e., the surface is not an ideal flat surface; the two sharp dents located at the positions measured with horizontal and vertical axis coordinates, ( $12 \mathrm{~mm}, 15 \mathrm{~mm}$ ) and (24 mm, 15 mm), are the real locations of impacts, and the inner damage is located underneath and around them.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-133_609_1504_262_291.jpg)

Figure 6-1 (a) Optical image and (b) ultrasonic image of the scanned area of the specimen.

### 6.2.2 Experimental Setup

A two-dimensional scan was performed on the specimen in water under pulse-echo mode over an area of 40 mm (scan axis) by 30 mm (index axis). A customer-designed ultrasonic scanner fabricated by ‘Inspection Technology Europe BV’ is used for the scan. The transducer chosen for this investigation is a focused immersion transducer with a manufacturer-provided central frequency of 30 MHz . The reasons to choose such a transducer are (i) that the focused beam can greatly improve spatial resolution of the images obtained from the scan; and (ii) that this type of transducer has a high systematic noise level which satisfies the condition which is intended to deal with in this work.

### 6.3 Data Processing

### 6.3.1 Reflection Signals

The typical reflection signals obtained in both unimpacted and impacted areas are compared in Figure 6-2. The front-surface reflection can be readily identified from the waveform in Figure 6-2 (a), but the back-surface reflection, which is typically the signal from which signal properties are extracted for defect characterization [8], cannot be identify. This is due to the low signal-to-noise ratio caused by both relatively high noise
level and low signal level. In such a case the reflection signal corresponding to the inner structure of the plate is windowed by first isolating the front-surface reflection and the expected back-surface reflection and then choosing the signal in between. This windowed signal is supposed to contains information of the inner defect of the composite plates because of its time domain location in which any possible reflection caused by inner defects will appear. In this study the windowed signal covering a time range from $38.5 \mu \mathrm{~s}$ to $39.6 \mu \mathrm{~s}$, and the following analysis will be based on this part of the reflection. In addition, the spectra of the two waveforms shown in Figure 6-2 (a) shown and compared in Figure 6-2 (b) are complicated due to the existence of strong noise, and it is hard to see the distinct difference which is useful for impact characterization.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-134_1022_1400_1239_332.jpg)

Figure 6-2 Comparison of the reflections from unimpacted area and impacted area in (a) time domain and (b) in frequency domain.

### 6.3.2 C-scan Representation

C-scan imaging of the scanned area based on the properties of reflection signal is an effective way to characterize the potential defects within the scanned area. From a Cscan image defect location, shape and size can be identified in two-dimensional manner, and damage severeness can also be indicated by the color intensity contrast to some extent. Color intensity contrast is a critical property of C-scan imaging and it originates from the difference of the extracted signal properties at different positions. All the results obtained in this study will be represented in the form of C-scan images.

### 6.3.3 Conventional Signal Property Extraction

When ultrasound goes through a composite plate, it will be both attenuated and dispersed. Despite the complicated mechanism of attenuation and dispersion imaging an area in a C-scan is quite easy as long as the extracted signal property is capable of showing the difference between undamaged area and damaged area. Conventionally, the signal properties to be extracted are either amplitude or time-of-flight (TOF) of the windowed signals. Amplitudes can be either the maximum or minimum amplitude of the widowed signal; and the TOF is can be the TOF the peak with maximum amplitude, the TOF to the trough with minimum amplitude, or the TOF to an amplitude threshold of the windowed signal. For the reflection signal obtained in ultrasonic pulse-echo mode the front-surface reflection is conventionally windowed for imaging the front surface such as the ultrasonic image shown in Figure 4-1 (b), the back-surface reflection windowed for imaging the inner structure because it goes through the whole plate twice in thickness direction and accordingly strongly affected by the inner structure. Normally, the backsurface reflection is the ideal signal for characterizing the defects inside the composite structure, but for this case the back-surface reflection is not available, and we have to
focus on the middle section of the signal between front-surface and back-surface reflections. Data properties based both on amplitude and TOF of the windowed signal will be used for imaging the defects in this study.

### 6.3.4 Spectral Signal Property Extraction

An ultrasound pulse generated by a transducer usually consists of many different frequency components that correspond to different wavelengths. When an incident sound pulse interacts with a composite plate, the plate works as a filter, which has different filtering effects on different frequency components due to the relative dimensions of the sound wavelength and the defect in the plate. Therefore, in frequency domain it is expected to find some frequency components that are filtered differently by unimpacted and impacted areas. In addition, in frequency domain the systematic noise, which normally has a limited spectral coverage, will be easy to isolated. Based on the above considerations the amplitudes of the different frequency components of the windowed signal are extracted. The spectra of the windowed signals obtained at an impacted position and an unimpacted position are shown in Figure 6-3. It can be observed that in the range of 8 MHz to 22 MHz the difference of two spectra is distinct and consistent. For a better view of the difference between reflection signals obtained from impacted area and umimpacted area, the time domain representation of a line scan over the whole range of the scan axis at the index position of 15 mm (B-scan) and its frequency domain representation are shown in Figure 6-4 (a) and (b) respectively. From the time domain representation, i.e., the B-scan in Figure 6-4 (a), it is hard to distinguish the impacted positions and the umimpacted ones due to the high-level background noise. However, in frequency domain as shown in Figure 6-4 (b) it is easier to see the difference of impacted and unimpacted areas especially at the low frequencies such as the range from around 8

MHz to 25 MHz. The C-scan image based on the frequency domain analysis will be shown later and compared with those obtained from time domain analysis.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-137_477_1437_473_304.jpg)

Figure 6-3 Spectrum of the reflection signal windowed from

$38.5 \mu \mathrm{~s}$

to

$39.6 \mu \mathrm{~s}$

.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-137_761_1437_1167_304.jpg)

Figure 6-4 (a) B-scan of the reflection signals windowed from

$38.5 \mu \mathrm{~s}$

to

$39.6 \mu$

s at the index position of 15 mm and (b) its spectral representation.

### 6.4 Results and Discussion

### 6.4.1 Conventional Characterization

The maximum amplitude, the minimum amplitude, the TOF to the peak with minimum amplitude and the TOF to the trough with the minimum amplitude of each windowed reflection are extracted and shown in the form of C-scan image in Figure 6-5.

It can be seen that the location, shape and size of the two defects can be identified from all the images, and that the two images based on TOF give the same results, and that the two images based on amplitude change also give the same results. Moreover, the results obtained from TOF and those from amplitude change are not completely same due to the difference in characterization mechanism. Concerning the severeness of the impacts only the images based on amplitude change shown in Figure 6-5 (a) and (c) can give some information through the color contrast. Although the color scale in Figure 6-5 (a) and (c) are opposite, they give the same results in the respect of impact severeness due to the fact that they show the same image contrast. These images will be compared later with those obtained using spectral technique.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-138_784_1419_1311_301.jpg)

Figure 6-5 C-scan images obtained based on (a) the maximum amplitude, (b) the minimum amplitude, (c) the TOF to the peak with maximum amplitude, and (d) the TOF to the trough with minimum amplitude of the windowed reflections.

### 6.4.2 Spectral Characterization

According to the observation in Figure 6-4 that in the frequency domain the difference between the unimpacted area and the impacted area is relatively distinct and
consistent, C-scan images were obtained at different frequencies and shown in Figure 6-6. In order to see the sensitivity of different frequency components to the defects images obtained at 5 MHz, 10 MHz, 15 MHz, 20 MHz, 25 MHz, 30 MHz, 35 MHz and 40 MHz are shown and compared in Figure 6-6. First, all these images except for the one in Figure 6-6 (a) are capable of showing the location, shape, size and severeness of the impact defect inside the composite plate as those shown in Figure 6-5. Second, all the images show the same location of the two impact defects, but the shape, size and color contrast of each image are slightly different. Although the detailed mechanism for the difference in defect shape, size and color contrast is complicated, it is easy to see that this difference results from the sensitivity of different frequency components to the same defects. Compared with the C-scan images obtained from the time-domain signal properties, i.e., amplitude change and TOF, the frequency-domain images give more information about the inner defects of the composite plates. In addition, it can be seen that the images in Figure 6-5 (b), (c), (e) and (f) have relatively higher color intensity at the damaged area and better contract than those obtained from time domain shown in Figure 6-4.

The image obtained at 5 MHz shown in Figure 6-6 (a) has very low color contrast because at this frequency the spectral amplitude of the ultrasound pulse is very low which can be confirmed by the observation of both Figure 6-3 and Figure 6-4 (b). Within the spectral coverage of the ultrasound all the images have distinct color contrast as shown in Figure 6-6 (b) to (f). Considering all the information shown by Figure 6-3, 6-4 (b) and 6-6 it can be concluded that there exits a sensitive frequency range, around 8-32 MHz, over which high quality images can be obtained to characterize the impact defects.

It is known that different frequency components of an ultrasound pulse with different wavelengths interact differently with an object of a specific size depending on the
relative size of the wavelength and the object. Therefore, from a filter’s point of view different frequency components have different sensitivity to the defect inside the plate. The similar but different images of the same defects shown in Figure 6-6 actually represent the defects from different perspectives, and the exact information about the defects can be obtained once the sensitivity of different frequency components to a defect with a fixed size can be quantitatively characterized.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-140_1568_1405_844_303.jpg)

Figure 6-6 C-scan images obtained based on the amplitudes of the frequency components at (a) 5 MHz, (b) 10 MHz, (c) 15 MHz, (d) 20 MHz, (e) 25 MHz, (f) 30 MHz, (g) 35 MHz, and (h) 40 MHz.

### 6.5 Conclusions

In this work impact defect characterization is investigated for the case in which unavoidable high-level noise is caused by the ultrasonic transducer used. Signal windowing is applied to obtain the signal corresponding to the inner structure of the composite plates. Conventional data property extraction methods, extreme amplitude technique and TOF technique, were applied for C-scan imaging. Spectral data property extraction technique is proposed and the obtained C-scan images are compared with those obtained with conventional methods.

The feasibility of the proposed spectral technique for impact defect characterization is illustrated. The spectral technique can work as an alternative method for characterizing defects under normal conditions and as a compulsory method for the cases with low signal-to-noise ratio signals. Compared with the conventional method the spectral method is promising to characterize the dimension of the defect structure, and gives a more complete representation of the defect details given the exact sensitivity of different frequency components to a defect with a fixed size.

## RESUME DU CHAPTRE VII

Les matériaux en plaques composites sont largement utilisés dans presque toutes les branches de l’industrie moderne et de la vie quotidienne. La caractérisation des défauts de ces plaques composites d’impact est d’un grand intérêt dans le contrôle de la qualité et de contrôle de la sécurité. Une variété de méthodes nondestructives est disponible à cet effet, le contrôle par ultrasons immersion est l’un d’entre eux. Ce dernier est connu pour sa grande fiabilité et d’efficacité. Dans ce chapitre, sont comparées plusieurs application pur immersion afin de caractériser les dommages de plaques de carbone / époxy d’impact. Deux plaques échantillons avec les dommages causés par l’impact contrôlé sont testés. Trois configurations de test sont discutées et plusieurs méthodes de traitement de données dans le domaine temporel et dans le domaine fréquentiel sont appliquées. La comparaison des résultats montre que, avec une combinaison optimale d’une configuration d’essai, le transducteur et la sélection de fréquences et des procédés de traitement des données, les défauts peuvent être plus facilement et plus présisement caractérisés que par les moyens conventionnels.

## CHAPTER VII

## COMPARISON OF DIFFERENT APPROACHES IN CHARACTERIZATION OF IMPACT DEFECTS OF COMPOSITE PLATES

### 7.1 Introduction

Characterization of impact defects of composite materials has been of great interest for a long time due to its importance in material health monitoring and control. Because of their complex inner structures and corresponding anisotropy in mechanical properties composite material defects cannot be detected and evaluated through standard procedures like isotropic metallic materials, and so different cases have to be treated differently.

Among different nondestructive testing (NDT) methods, ultrasonic NDT has strong advantages in many aspects and it has been widely used in both industrial application and research [1-3]. Similar sub-techniques have been compared in order to both confirm the results obtained and to evaluate the reliability of different methods [1]. Many variants of ultrasonic NDT techniques such as ultrasonic burst phase thermography [2] have still been proposed and tested.

Inspired by some summary work in this area [4] the authors think it worthwhile to compare different techniques in characterizing impact defects for the purpose of optimizing the practical testing process. In this work different approaches of immersion ultrasonic NDT technique are compared.

### 7.2 Experiments

### 7.2.1 Sample Preparation

Two carbon/epoxy plates with the dimensions of 120mm long, 120 mm wide and 2.35 mm thick are tested in this work. The damages of the plates were made by designed impacts: a 50 g impactor with two blades of 0.385 mm wide impacted Sample I at a speed of 9.35 m/s and Sample II at a speed of 18.27 m/s. It is reasonable that Sample I is less severely damaged and its impact defects are correspondingly harder to be detected than Sample II. This expectation is confirmed by the characterization in this work, and for the purpose of reducing the redundancy most of the illustrations will be focused on the results obtained from Sample I.

### 7.2.2 Transducer Selection

For ultrasonic investigations the choice of frequency is crucial. High frequency ultrasounds result in smaller wavelengths and therefore higher sensitivity for detecting small damages. In terms of improving detection accuracy for small damages higher frequency is generally desired. However, due to the nature of composite material, there are point-to-point variations in material properties such as mass density, volume composition; in another words, the material is not homogenous. This limits the application of high frequency ultrasound because high frequency increases the difficulty in discriminating the damaged area of final C-scan image caused by the material property change and by the real defect, that is, high frequency ultrasound actually reduces detection accuracy. Practically, low frequency ultrasound works more accurately in identifying damaged areas in terms of both their locations and sizes. Therefore, for the purpose of improving detection sensitivity and accuracy a compromise has to be made in order to obtain the best possible characterization of the samples. In this work 5 MHz
transducers are chosen taking advantage of their smaller pulse length in time domain which will lead to clearly separated waves received after going through the samples. The importance of these clearly separated waves will be discussed later in this paper. In addition, for the purpose of comparison, two different types of immersion transducers, one focused with spherical focus of 4 inches and one unfocused, are chosen for the current work.

### 7.2.3 Experimental Configurations

In this work three experimental configurations are applied for C-scans on an area of 40 mm x30 mm covering the impacted positions: pitch-catch or transmission-through mode, pulse-echo mode and pseudo pulse-echo mode (Figure 7-1). As the most widely used modes for ultrasound testing, pitch-catch and pulse-echo modes are chosen due to the convenience of operation and their wide validity in other testing.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-145_688_832_1585_616.jpg)

Figure 7-2 Schematic of pseudo pulse-echo mode at the critical angle

$\theta_{\boldsymbol{c}}$

.

A third mode called pseudo pulse-echo mode is also chosen for the purpose of comparison. The schematic of this mode is shown in Figure 7-1. In the pseudo pulse-
echo mode two transducers (an emitter and a receiver) are set at an angular position which corresponds to a critical angle of the sample plates. The critical angles of the sample plates are measured in a polar scan shown in Figure 7-2. In this work, the second critical angle ( $\theta_{c}=30^{\circ}$ ) is used instead of the first one ( $\theta_{c}=9^{\circ}$ ) for the convenience of practical testing operation.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-146_671_1335_837_363.jpg)

Figure 7-2 Absolute amplitude of transmitted wave through the sample plates at different indent angles.

### 7.3 Data Processing

In this section the response signals obtained in the scan using three experimental modes are analyzed first, and followed are the detailed data analysis approaches.

### 7.3.1 Response signals

The time-domain response signals obtained at both unimpacted area and impacted area in three modes are shown in Figure 7-3. It can be observed that at the unimpacted area three response waves are detected for pitch-catch mode and pulse-echo mode and two detected for pseudo pulse-echo mode. This is logical result based on the fact that composite plates have small thicknesses. This characteristic makes it possible to extract
more information concerning the inner defects by analyzing the second and even the third response signals because they go through the plates more times than the first one and accordingly contain more information about the inner structures.

It can also be observed that for both pulse-echo and pseudo pulse-echo modes, the interval between the first response wave and the second one experiences more changes than other time ranges. This fact can also be used in data processing for the purpose of obtaining effects of inner destruction caused by impact.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-147_1513_994_948_517.jpg)

Figure 7-3 Comparison of response signals at unimpacted area and impacted area for (a) pitch-catch mode, (b) pulse-echo mode and (c) pseudo pulse-echo mode.

### 7.3.2 Time Domain Data Analysis

The properties usually used to characterize material properties in ultrasonic nondestructive testing are time-of-flight (TOF) and amplitude. The damaged structure in the plate can change sound velocity and phase and this can be observed in time-domain through the changes of TOF for specific wave properties like maximum peak, minimum peak and preset threshold. Also, the damaged inner structure can attenuate sound energy leading to decrease in amplitudes. This effect is evaluated in this work by recording the amplitudes of positive peaks and negative peaks and their maximum absolute values. Frequency-domain data analysis

### 7.3.3 Frequency Domain Data Analysis

As we know different frequency components of a bulk sound beam have different sensitivity to the same structure. Taking advantage of the large frequency range of about 6 MHz , from 1 MHz to 7 MHz, produced by the transducer used, the impact defect can be examined at different frequencies.

Figure 7-4 shows the comparison of frequency responses between a wave obtained from umimpacted area and one from the impacted area in pitch-catch mode. It can be observed that due to the limited thickness, oscillating components appearing at a period of around 0.66 MHz in the spectrum of a signal obtained from unimpacted area are not obvious in the spectrum of the signal obtained from impacted area. This leads to a relatively large difference in amplitude at those frequencies and they are used in this work to evaluate the effects of damaged inner structure. In addition, the same phenomenon can be observed in pulse-echo mode.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-149_601_1249_315_390.jpg)

Figure 7-4 Comparison of the spectrums of response signals at unimpacted area and impacted area for pitch-catch mode.

### 7.4 Results and Discussion

It is easy to understand that it is more difficult and challenging to detect the impact damages in Sample 1 because it was applied by much less external impact compared to Sample 2. Therefore, for the purpose of comparing the feasibility and sensitivity of the proposed approaches, only the results obtained from Sample 1 are shown in this section.

### 7.4.1 TOF and Amplitude

In order to compare the feasibility of the most commonly used wave characteristics, TOF and amplitude, in characterizing the impact defect inside the sample plates, both amplitudes and TOFs in a 40mmX30mm C-scan are shown in Figure 7-5. It can be easily observed that amplitude is much more sensitive to the inner impact damage of the sample composite plates than TOF. This is probably due to the fact that the thicknesses of the samples are small and so there is no enough length for sound speed change being detected and clearly visualized in the form of C-Scan. The reason that amplitude has
strong sensitivity to impact defects is probably that the inner structures of the damaged area are irregular and this causes more energy loss by sound diffraction.

Since amplitude has strong sensitivity in detecting impact defects, the following discussion will focus on amplitude change in both time-domain and frequency-domain.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-150_1196_1504_642_320.jpg)

Figure 7-5 Comparison of the effects of amplitude and TOF in characterizing the impact defect for Sample 1. (a), (b) and (c) are respectively the amplitudes of absolute values, maximum peaks and negative peaks of the first response wave at each position; (d), (e) and (f) are respectively the TOFs to negative peaks, positive peaks and preset threshold.

### 7.4.2 Time Domain Attenuation

As noticed in Figure 7-3 in pitch-catch mode there are three waves in time-domain after going through the plates. Their amplitudes are different due to the attenuation they experience in the process of traveling within the plate: the first wave goes through the whole thickness once, the second one three times and the third one five times. It is
logical that the more times a wave going through the plates, the more attenuation they get and the more information they carry about the inner structures of the plates. However, the more attenuated the waves are, the smaller the ratio of signal to noise are and this makes the third wave less sensitive to the inner structural defects.

The difference stated above can be observed in Figure 7-6 through comparison of the amplitudes of the maximum peaks and minimum peaks of the first wave and the second wave obtained in pitch-catch mode. The defect areas obtained from the second wave is much larger than those obtained from the first wave. This does not mean that one of them is less accurate and less reliable in characterizing the inner defects, but they carry the information of the same defects at different levels. Obviously, the results obtained from the second wave tell us more.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-151_876_1544_1405_298.jpg)

Figure 7-6 Comparison of the amplitude sensitivity to impact defects of the first wave and the second wave in pitch-catch mode. (a) and (b) are respectively the amplitudes of the maximum peaks and minimum peaks of the first wave; while (c) and (d) are those of the second waves.

For pitch-catch mode the first wave carries enough information to characterize the defects because it goes through the plate once, but for pulse-echo mode and pseudo pulse-echo mode the first wave is mainly specular reflection from the plate surface and therefore not sensitive to the inner defects. For these two cases the signals in the interval between the first and the second waves are more sensitive to the defect because they are mainly the reflection from the inner defects in the plates before the sound reaches the bottom surfaces of the plates. The maximum amplitudes of the signals in the intervals are compared with those obtained from the second wave in pulse-echo mode and the whole waves in the pseudo pulse-echo mode in Figure 7-7. It can be seen that the interval signals give clear image about the shape of the defects.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-152_917_1523_1299_320.jpg)

Figure 7-7 Comparison of the amplitude sensitivity to impact defects of the signal in the interval between the first two waves in (a) pulse-echo mode and (d) pseudo pulse-echo mode and the second wave in (a) pulse-echo mode and the first wave in (b) pseudo pulseecho mode.

### 7.4.3 Frequency Domain Attenuation

Based on the fact that sound waves of different frequency have different wavelength, and that sound with different wavelengths have different sensitivity to the defects in the thickness direction, the attenuation of sound energy in frequency-domain may give us information concerning the defect levels at different depth of the plates although it is hard to identify the relationship between the depth and the frequency.

In Figure 7-8 the attenuation of sound at six different frequencies are shown in the form of spatial C-scan. The frequencies chosen here are those corresponding to the peaks in Figure 7-4. The interesting thing is that they all confirm the position of the defects, but the damage level (indicated by color) of the defect relative to the neighborhood areas are different. This is reasonable because at different depth, the damage levels are different. For all the three modes tried in this study, frequency-domain analysis works well as shown in Figure 8.

### 7.4.4 Effect of Transducer Type

Through comparison of the results obtained with unfocused transducer and focused transducer, it can be observed that the focused transducer can give better relatively stronger signals and more clear images. Therefore, in this kind of damage detecting focused transducers are recommended.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-154_1181_1518_279_315.jpg)

Figure 7-8 Comparison of the responses of maximum amplitude to the impact defects in pitch-catch mode at different frequency components: (a) 1.98 MHz, (b) 2.67 MHz, (c) 3.30 MHz, (d)

$\mathbf{3 . 9 3 ~ M H z ,}$

(e)

$\mathbf{4 . 5 8} \mathbf{~ M H z}$

and (f)

$\mathbf{5 . 2 5 ~ M H z}$

.

### 7.5 Conclusion

All the three experimental configurations work efficiently in characterization of the impact defects inside the composite plates. Due to the small thickness and the relatively narrow pulse width, more than one wave are obtained and this offers more options in choosing signals from which defect information can be extracted. It is observed that the first two waves carry defect information of different levels in pitch-catch modes and that the signals lying in the interval between the first two waves in pulse-echo mode and pseudo pulse-echo mode work more efficient that other waves.

It is also observed that time-of-flight (TOF) is less sensitive than amplitude in indicating defects. In both time-domain and frequency-domain amplitude can well indicate the defect information. Furthermore, the amplitude changes in frequency due to different sound attenuation at different areas carry information of defects at different depth. It is worth exploring the relationship between the depth and the frequency which promises the possibility of obtaining a three-dimensional representation of defects through a simple C-scan.

## RESUME DU CHAPTRE VIII

Dans ce chapitre, les traveux de recherche dans les deux domaines, l’étude de l’interaction des ultrasons avec des structures périodiques et la caractérisation du défaut cause par l’impact sur les plaques composites sont résumes. Le chapitre se termine par une suggestion d’éventuels travaux de recherche qui pouraient constituer une suite aux presents travaux.

## CHAPTER VIII SUMMARY AND FUTURE WORK

There are many potential areas of exploration that can fall into the two categories of investigation, interaction of ultrasound with periodic structures and interaction of ultrasound with composite materials, which are presented in this work. However, only a few areas have been investigated and presented in thesis. This chapter serves as a summary of the main scientific contributions made in these areas and it also presents opportunities that exist in these areas for future work.

### 8.1 Concluding Summary: The Investigation of the Interaction of Ultrasound with Periodic Structures

Two physical phenomena of diffraction on the periodic surface, i.e., acoustic Wood anomaly and sub-harmonic diffraction, and two applications of ultrasound in nondestructive testing of periodic structures are investigated under the topic of the interaction of ultrasound with periodic structures.

In the investigation of acoustic Wood anomaly presented in Chapter III spectral peak as a form of spectral anomaly is experimentally observed. In the literatures the only form of spectral anomalies in the reflection spectrum is sharp spectral dips and no spectral peak has ever been reported. On the theoretical side a complete review of the existing theories about the physical origin of acoustic Wood anomaly is presented. After the careful examination of all the aspects of the existing theory based on the experimental results obtained from a corrugated interface with a rectangular profile, the physical process of the occurrence of a spectral anomaly is described as a process of four steps: (i) the first mode conversion on the corrugated surface from a propagating bulk incident wave to surface-type wave at a transition frequency, (ii) generation of surface resonance
on the surface corrugation, (ii) the second mode conversion on the corrugated surface from the surface-type wave mode back to a propagating wave with a single frequency (resonant frequency), and (iv) the virtual or physical interface of the direct reflection from the corrugated surface and the twice mode-converted propagating wave. The phase shift of the frequency components at the resonant frequency between the direct reflection and the twice mode-converted wave determines the type of spectral anomaly: spectral peaks resulting from a phase enhancing effect or spectral dips resulting from a phase cancelling effect. Thus, the physical origin of acoustic Wood anomaly can be explained explicitly.

The significance of the investigation of the second diffraction phenomenon, the socalled sub-harmonic diffraction, is the experimental observation of the abnormal diffraction patterned that cannot be explained by the classical grating equation. The experimental proof of the existence of such a diffraction phenomenon is robust because it has been observed from the experimental results obtained using four different corrugated silicon samples and three different corrugated brass samples and the experiments are performed in different configurations. Although no definite physical explain has been given for the observation, explorations of the possible theories have been made. The possible physical observation in optical diffraction that follow the same principle of the sub-harmonic diffraction is predicted for further investigation in optics.

In the nondestructive characterization of the geometry of a periodic surface with a rectangular profile both robust theoretical discussion and experimental exploration are made. In the theoretical exploration the effects of the beam characteristics such as beam bandwidth and beam diameter on the geometric characterization are quantitatively analyzed; while the effects of the beam properties such as central frequency and the scanning resolutions are discussed qualitatively. The conclusions obtained from the
theoretical discusses have wide application in all the similar investigations. The experimental results in the form C-scan images of the corrugated surface show good agreement with the optical microscopic observations.

The novelty of the nondestructive evaluation of the corrugation periodicity of the stacked cylindrical rods lies in both the application of air-coupled ultrasonic technique and the application of acoustic Bragg diffraction. The fact that highly accurate measurements are obtained using relatively low quality air-coupled transducer promises it potential application in industrial world at a low cost.

### 8.2 Concluding Summary: The Investigation of the Ultrasonic Characterization of Impact Defects of Composite Plates

Two explorations have been made for characterizing the impact defects of composite plates: the investigation in the spectral data analysis for C-scan imaging and the investigation of comparison of different approaches for impact defect characterization. The first exploration deals with the situation in which unavoidable high-level noise caused by the data acquisition system corrupts received signal for defect detection. It has been shown that in frequency domain it is easy to exclude the effects of noise to the final results. Moreover, the frequency domain data analysis provides a way to detect the dimension of defects due to the fact that different frequency components have different sensitivity to a defect of fixed size.

The comparison of different approaches of immersion ultrasonic technique in impact defect characterization shows that there is no a universal method for the characterization of all situations and each case has to be treated specifically even in the small area of immersion ultrasonic testing. The investigation suggests that with an optimized combination of testing configuration, transducer and frequency selection, and data processing methods, the defects can be more accurately and easily characterized.

### 8.3 Future Work for the Interaction of Ultrasound with Periodic Structures

In Chapter II the periodic surfaces whose corrugation height is smaller than the spatial resolution of the incident beam has been categorized as the case in which the corrugation geometry cannot be characterized using the proposed method. The reason is that the corrugation height is too small to make the echoes from the plateau and valley surfaces of the corrugation separate from each other in time domain, i.e., echo overlapping occurs. In practice such corrugations also need to be geometrically characterized, and a solution should be obtained. One possible solution is applying the so-called pulsed ultrasonic comb filtering effect to this case. Although the phase shift relationship obtained from the pulsed ultrasonic comb filtering effect is able to measure the thickness of thin plates with a very high accuracy [1] a detailed investigation is still necessary when applying the existing relationship to this case.

Another possible future work is to apply the same technique proposed in Chapter III to the nondestructive testing (NDT) of concealed corrugations. The need for developing such a technique arises from the practical application such as NDT of pipes with inner corrugation or roughness. The biggest challenge of developing high frequency ultrasonic technique for concealed corrugation characterization is the attenuation of the incident sound beam. Therefore, careful choice of ultrasound frequency should be aware of.

Chapter IV illustrates the physical process occurs on the corrugated surface and shows the mode conversion caused by the corrugated surface. The potential application of this physical effect is to generate surface acoustic wave on non-piezoelectric materials [2, 3] for a new type of transducer or sensor. This topic is very interesting and worth for future investigation.

### 8.4 Future Work for the Characterization of Impact Defects of Composite Plates

The spectral data analysis for impact defects characterization promises the possibility of characterizing the defect dimensions together with the lateral position, shape and severenss of the damaged area which can be obtained using the conventional temporal data analysis. However, the quantitative relationship between the frequency and the defect dimension has not yet been obtained. It is a very interesting and important work to
find the effects of different frequencies of incident beam on a defect with fixed dimension which has already been observed in the work presented in Chapter VI.

A possible method to investigate the relationship between frequency and defect dimension, or frequency sensitivity to defect, is to make a sample with defects of different size such as holes with different diameters and then analyze the spectral response of the same incident beam to different defect. Such samples have been fabricated and one of them is shown in Figure 8-1. The material of the sample is aluminum and the diameters of the holes on the far left column are 1.0 mm, 1.5 mm and 2.0 mm from top to bottom, the diameters of the holes on the second column on the left side 2.0 mm, 1.5 mm, and 1.0 mm from top to bottom, and the diameters of the holes on the right side of the sample 2.0 mm, 1.5 mm, 1.0 mm, 1.0 mm and 0.8 mm from left to right.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-161_221_1109_1491_479.jpg)

Figure 8-1 A aluminum block with holes of different diameters.

A line B-scan has been performed on this sample in a pulse-echo configuration for obtaining the echoes reflected from the defects. And the B-scan image and the corresponding frequency domain representation are shown in Figure 8-2 (a) and (b) respectively. Based on this kind of experimental results the following topics should be investigated in order to have a better idea of the frequency sensitivity to defects: (i) the mechanism of response difference of different frequency components to the same defect; (ii) the mechanism of response difference of the same frequency component to different
defects; (iii) the effect of the defects of different size overlapping in the wave propagation direction on the frequency response.

![](2018_Liu_DrThesis_Interaction%20of%20ultrasound%20with%20p/images1b644986-e55c-4d89-9d09-92bc1a6cffc4-162_722_1482_544_279.jpg)

Figure 8-2 (a) B-scan of the reflections from the designed holes and (c) its frequency domain representation.

## REFERENCES

## Citations in Chapter I: Introduction

[1] J. Rayleigh, The Theory of Sound. New York: Macmillan & Co., 1896.
[2] J. M. Claey, O. Leroy, A. Jungman, and L. Adler, “Diffraction of ultrasonic waves from periodically rough liquid-solid surface”, J. Appl. Phys. 54, 5657 (1983).
[3] A. Jungman, O. Leroy, G. Quentin and K. Mampaert, “Theoretical and experimental study of ultrasonic surface modes at a solid-fluid periodic interface”, J. Appl. Phys. 63, 4860 (1988).
[4] K. Mampaert and O. Leroy, “Reflection and transmission of normally incident ultrasonic waves on periodic solid-liquid interfaces”, J. Acoust. Soc. Am. 83, 1390 (1988).
[5] A. Jungman, L. Adler, and G. Quentin, “Ultrasonic anomalies in the spectrum of acoustic waves diffracted by periodic interfaces”, J. Appl. Phys. 53, 4673 (1982).
[6] R. F. Humphryes and E. A. Ash, “Acoustic bulk-surface-wave transducer”, Electron. Lett. 5, 175 (1969).
[7] E. A. Ash, R. M. de la Rue, and R. F. Humphryes, “Microsound surface waveguide”, IEEE Trans. Microwave Theory Tech. 17, 882 (1969).
[8] M. A. Breazeale and M. A. Torbett, “Backward displacement of waves reflected from an interface having superimposed periodicity”, Appl. Phys. Lett. 29 (8), 456-458 (1976).
[9] N. F. Declercq, J. Degrieck, R. Briers, O. Leroy, “Theoretical verification of the backward displacement of waves reflected from an interface having superimposed periodicity”, Appl. Phys. Lett. 82 (15), 2533-2534 (2003).
[10] A. Teklu, M. A. Breazeale, N. F. Declercq, R. D. Hasse and M. S. McPherson, “Backward displacement of ultrasonic waves reflected from a periodically corrugated interface”, J. Appl. Phys. 97, 084904 (2005).
[11] S. W. Herbison and N. F. Declercq, “Angular and frequency spectral analysis of the ultrasonic backward beam displacement on a periodically grooved solid”, J. Acoust. Soc. Am. 126 (6), 2939-2948 (2009).
[12] S. W. Herbison and N. F. Declercq, “Observation of ultrasonic backward beam displacement in transmission through a solid having superimposed periodicity”, Appl. Phys. Lett. 97, 041908 (2010).
[13] A. Jungman, L. Adler, and G. Quentin, “Ultrasonic anomalies in the spectrum of acoustic waves diffracted by periodic interfaces”, J. Appl. Phys. 53, 4673 (1982).
[14] A. Jungman, L. Adler, J. D. Achenbach, and R. Roberts, “Reflection from a boundary with periodic roughness: Theory and experiment”, J. Acoust. Soc. Am. 73, 1025 (1983).
[15] J. M. Claey, O. Leroy, A. Jungman, and L. Adler, “Diffraction of ultrasonic waves from periodically rough liquid-solid surface”, J. Appl. Phys. 54, 5657 (1983).
[16] A. Jungman, O. Leroy, G. Quentin and K. Mampaert, “Theoretical and experimental study of ultrasonic surface modes at a solid-fluid periodic interface”, J. Appl. Phys. 63, 4860 (1988).
[17] K. Mampaert and O. Leroy, “Reflection and transmission of normally incident ultrasonic waves on periodic solid-liquid interfaces”, J. Acoust. Soc. Am. 83, 1390 (1988).
[18] J. F. Liu, , N. F. Declercq, “Air-Coupled ultrasonic investigation of stacked cylindrical rods”, J. Acoust. Soc. Am. 131 (6), 4500-4507 (2012).

## Citations in Chapter II: Acoustic Wood Anomaly Phenomenon

[1] Lord Rayleigh, Theory of Sound, Dover Publications, Vol. 2, New York, pp. 89-96, 1945.
[2] B. A. Lippmann, “Note on the theory of grating”, J. Opt. Soc. Am. 43, 408 (1953).
[3] C. Eckart, “The scattering of sound from the sea surface”, J. Acoust. Soc. Am. 25, 566 (1953).
[4] D. Mintzer, “Discussion of the paper by C. Eckart on sea surface scattering”, J. Acoust. Soc. Am. 25, 1015 (1953).
[5] J. W. Miles, “On nonspecular reflection at a rough surface”, J. Acoust. Soc. Am. 26, 191 (1954).
[6] W. C. Meecham, “Variational method for the calculation of the distribution of energy reflected from a periodic suface. I”, J. Appl. Phys. 27, 361 (1956).
[7] E. O. LaCase, Jr., “Measurement of sound reflection from a rigid corrugated surface”, J. Acoust. Soc. Am. 33, 1772 (1961).
[8] J. L. Uretsky, “Reflection of a plane sound wave from a sinusoidal surface”, J. Acoust. Soc. Am. 35, 1293 (1963).
[9] J. L. Uretsky, “The scattering of plane waves from periodic surface”, Ann. Phys. 33, 400 (1965)
[10] J. T. Fokkema and P. M. van den Berg, “Elastodynamic diffraction by a periodic rough surface (stress-free boundary)”, J. Acoust. Soc. Am. 62, 1095 (1977).
[11] J. T. Fokkema, “Reflection and transmission of elastic waves by the spatially periodic interface between two solids”, Wave Motion 2, 375 (1980).
[12] A. Wirgin, “Reflection from a corrugated surface”, J. Acoust. Soc. Am. 68, 692 (1980).
[13] J. T. Fokkema, “Reflection and transmission of acoustic waves by the periodic interface between a solid and a fluid”, Wave Motion 3, 145 (1981).
[14] S. L. Chuang and R. K. Johnson, “Acoustic wave scattering from a fluid-solid periodic rough surface”, J. Acoust. Soc. Am. 71, 1368 (1982).
[15] A. W. Sáenz, “Scattering by periodic surfaces”, J. Math. Phys. 23, 1115 (1982).
[16] J. M. Chesneaux and A. Wirgin, “Reflection from a corrugated surface revisited”, J. Acoust. Soc. Am. 96, 1116 (1994).
[17] E. O. LaCase, Jr. and P. Tamarkin, “Underwater sound reflection from a corrugated surface”, J. Appl. Phys. 27, 138 (1956).
[18] J. J. Proud, Jr., P. Tamarkin, and W. C. Meecham, “Reflection of sound from a surface of sawtooth profile”, J. Appl. Phys. 28, 1298 (1957).
[19] E. O. LaCase, Jr., B. D. McCombe, and R. L. Thomas, “Measurement of sound reflection from a rigid corrugated surface”, J. Acoust. Soc. Am. 33, 1768 (1961).
[20] R. W. Wood, “On a remarkable case of uneven distribution of light in a diffraction grating spectrum”, Philos. Mag. 4, 396 (1902).
[21] Lord Rayleigh, “Note on the remarkable case of diffraction spectra described by Prof. Wood”, Phil. Mag. 14, 60 (1907).
[22] Lord Rayleigh, “On the dynamic theory of gratings”, Proc. Roy. Soc. A79, 399 (1907).
[23] A. Jungman, L. Adler, and G. Quentin, “Ultrasonic anomalies in the spectrum of acoustic waves diffracted by periodic interfaces”, J. Appl. Phys. 53, 4673 (1982).
[24] A. Jungman, L. Adler, J. D. Achenbach, and R. Roberts, “Reflection from a boundary with periodic roughness: Theory and experiment”, J. Acoust. Soc. Am. 73, 1025 (1983).
[25] J. M. Claey, O. Leroy, A. Jungman, and L. Adler, “Diffraction of ultrasonic waves from periodically rough liquid-solid surface”, J. Appl. Phys. 54, 5657 (1983).
[26] A. Jungman, O. Leroy, G. Quentin and K. Mampaert, “Theoretical and experimental study of ultrasonic surface modes at a solid-fluid periodic interface”, J. Appl. Phys. 63, 4860 (1988).
[27] K. Mampaert and O. Leroy, “Reflection and transmission of normally incident ultrasonic waves on periodic solid-liquid interfaces”, J. Acoust. Soc. Am. 83, 1390 (1988).
[28] K. Mampaert, P. B. Nagy, O. Leroy, L. Adler, A. Jungman, and G. Quentin, “On the origin of the anomalies in the reflected ultrasonic spectra”, J. Acoust. Soc. Am. 86, 429 (1989).
[29] R. F. Humphryes and E. A. Ash, “Acoustic bulk-surface-wave transducer”, Electron. Lett. 5, 175 (1969).
[30] E. A. Ash, R. M. de la Rue, and R. F. Humphryes, “Microsound surface waveguide”, IEEE Trans. Microwave Theory Tech. 17, 882 (1969).
[31] M. A. Breazeale and M. A. Torbett, “Backward displacement of waves reflected from an interface having superimposed periodicity”, Appl. Phys. Lett. 29, 456 (1976).
[32] S. W. Herbison and N. F. Declercq, “Angular and frequency spectral analysis of the ultrasonic backward beam displacement on a periodically grooved solid”, J. Acoust. Soc. Am. 126, 2939 (2009).
[33] M. A. Breazeale, L. Adler, and G. W. Scott, “Interaction of ultrasonic waves incident at the Rayleigh angle onto a liquid-solid interface”, J. Appl. Phys. 48, 503 (1977).
[34] J. Liu and N. F. Declercq, “Time-frequency analysis of Wood anomalies in acoustics”, Proceedings of Meetings on Acousitcs 19, 2013, pp. 055075.
[35] S. R. Roberts, J. D. Achenbach, R. T. Ko, L. Adler, A. Jungman, and G. Quentin, “Beam splitting at the reflection of elastic waves by a periodic surface profile”, J. Acoust. Soc. Am. 74, 1638 (1983).
[36] R. Roberts, J. D. Achenbach, R. Ko, L. Adler, A. Jungman, and G. Quentin, “Reflection of a beam of elastic waves by a periodic surface profile”, Wave Motion 7, 67 (1985).

## Citations in Chapter III: Sub-harmonic Diffraction Phenomenon

[1] D. G. Hall, “Optical wave-guide diffraction grating: coupling between guided modes”, Progress in Optics 29, 1-63 (1991).
[2] J. D. Freeze and R. H. Selfridge, “D-fiber holographic diffraction gratings”, Optical Engineering 32 (12), 3267-3271 (1993).
[3] S. Singh, “Diffraction gratings: aberrations and applications”, Optics and Laser Technology 31 (3), 195-218 (1999).
[4] J. N. McMullin, R. G. DeCorby and C. J. Haugen, “Theory and simulation of a concave diffraction grating demultiplexer for coarse WDM systems”, Journal of Lightwave Technology 20 (4), 758-765 (2002).
[5] P. Pottier and M. Packirisamy, “Design and properties of concave diffraction gratings based on elliptical Bragg mirrors”, Journal of Lightwave Technology 31(12), 1890-1898 (2013).
[6] Z. Q. Wang, S. H. Zhou and C. H. Wang, “Diffraction of SAW by acoustic grating”, IEEE Transactions on sonics and ultrasonics 32 (1), 86 (1985).
[7] D. Brill and G. C. Gaunaurd, “Identification of cylindrical-shells with sets of reinforcing ribs by their acoustic Bragg-diffraction (grating) patterns”, Applied Acoustics 45 (4), 321-334 (1995).
[8] D. J. Dieleman, D. J. Koenderink, A. F. M. Arts and H. W. de Wijn, “Diffraction of coherent phonons emitted by a grating”, Physical Review B 60 (21), 14719-14723 (1999).
[9] N. F. Declercq, J. Degrieck and O. Leroy, “On the theoretical possibility to apply an acoustic diffraction grating as a complex frequency filter device for electronic signals”, Ultrasonics 43 (9), 764-768 (2005).
[10] J. Liu, N. F. Declercq, “Ultrasonic geometrical characterization of periodically corrugated surfaces”, Ultrasonics, 53, 853-861 (2013).
[11] J. Liu, N. F. Declercq, “Air-Coupled Ultrasonic Investigation of Staked Cylindrical Rods”, J. Acoust. Soc. Am. 131 (6), 4500-4507 (2012).

Citations in Chapter IV: Air-Coupled Ultrasonic Investigation of Staked Cylindrical Rods
[1] S. W. Herbison, J. M. Vander Weide, N. F. Declercq, “Observation of ultrasonic backward beam displacement in transmission through a solid having superimposed periodicity”, Appl. Phys. Lett. 97, 041908 (2010).
[2] S. W. Herbison, N. F. Declercq, M. Breazeale, “Angular and frequency spectral analysis of the ultrasonic backward beam displacement on a periodically grooved solid”, J. Acoust. Soc. Am. 126, 2939-2948 (2009).
[3] N. F. Declercq, K. Dewijngaert, K. Vanderhaeghe, P. Verleysen, “An acoustic diffraction study of a specifically designed auditorium having a corrugated ceiling: Alvar Aalto’s lecture room”, Acta Acust. United Acust. 97, 599-606 (2011).
[4] J. A. C. Calleja, N. F. Declercq, “The acoustic raindrop effect at Mexican Pyramids: the architects’ homage to the rain god Chac?”, Acta Acust. United Acust. 95, 849-856 (2009).
[5] N. F. Declercq, C. S. A. Dekeyser, “Acoustic diffraction effects at the Hellenistic amphitheater of Epidaurus: seat rows responsible for the marvelous acoustics”, J. Acoust. Soc. Am. 121, 2011-2022 (2007).
[6] W. L. Bragg, J. J. Thomson, “The diffraction of short electromagnetic waves by a crystal”, Proc. Cambridge Philos. Soc. 17, 43-57 (1914).
[7] Y. S. Zhang, S. P. Kuo, “Bragg scattering measurement of atmospheric plasma decay”, Int. J. Infrared Milli. 12, 335-343, (1991).
[8] P. McNicholl and H.J. Metcalf, “Synchronous cavity mode and feedback wavelength scanning in dye laser oscillators with gratings”, Appl. Optics 24 (17), 2757-2761 (1985).
[9] R. S. Speer, G. C. Wetsel, “Measurement of anisotropy of ultrasonic-attenuation of longitudinal-wave in CAF2 using method of Bragg scattering”, Bull. Am. Phys. Soc. 22, 438-438 (1975).
[10] D. J. Haumschild, D. L. Carlson, “An ultrasonic Bragg scattering technique for the quantitative characterization of marbling in beef”, Ultrasonics 21, 226-2335 (1983).
[11] B. H. Houston, J. A. Bucaro, D. M. Photladis, “Broad-band acoustic scattering from a ribbed shell”, J. Acoust. Soc. Am. 98, 2851-2853 (1995).
[12] C. S. Hayek, I. W. Schurman, J. H. Sweeney, C. A. Boyles, “Azimuthal dependence of Bragg scattering from the ocean surface”, J. Acoust. Soc. Am. 105, 2129-2141 (1999).
[13] L. Goodman, J. Oeschger, D. Szargowicz, “Ocean acoustics turbulence study-acoustic scattering from a buoyant axisymmetrical plume”, J. Acoust. Soc. Am. 91, 3212-3227 (1992).
[14] M. Naciri and C. C. Mei, “Strong Bragg scattering of low-frequency sound from a line source in shallow-water 1. One uniform surface-wave”, J. Acoust. Soc. Am. 94, 1598-1608 (1993).
[15] C. S. Hayek, I. W. Schurman and J. H. Sweeney, “Azimuthal dependence of Bragg scattering from the ocean surface”, J. Acoust. Soc. Am. 105, 2192-2141 (1999).
[16] R. Briers, O. Leroy, O. Poncelet, “Experimental verification of the calculated diffraction field generated by inhomogeneous waves obliquely incident on a periodically rough liquid-solid boundary”, J. Acoust. Soc. Am. 106, 682-687 (1999).
[17] R. Lim and I. C. Paustian, J. L. Lopes, “Acoustic transmission across a roughened fluid-fluid interface”, J. Acoust. Soc. Am. 109, 1367-1383 (2001).
[18] E. Danicki, “Generation and Bragg reflection of surface acoustic-wave in nearly periodic system of elastic metal strips on piezoelectric half-space”, J. Acoust. Soc. Am. 93, 116-131 (1993).
[19] E. J. Danicki, “Surface acoustic wave diffraction in spectral theory of interdigital transducers”, J. Acoust. Soc. Am. 114, 831-820 (2003).
[20] A. Krynkin, O. Umnova, A. Y. B. Chong, S. Taherzadeh, K. Attenborough, “Predictions and measurements of sound transmission through a periodic array of elastic shells in air”, J. Acoust. Soc. Am. 128, 3496-3506 (2010).
[21] D. Sutter-Widmer, S. Deloudi, W. Steurer, “Prediction of Bragg-scattering-induced band gaps in phononic quasicrystals”, Phys. Rev. B 75, 094304 (2007).
[22] O. Leroy, R. A. Mertens, “Theoretical acoustooptics in Belgium”, Opt. Eng. 31, 2048-2061 (1992).
[23] A. S. Sliwinski, “Acoustooptics in Poland”, Opt. Eng. 31, 2062-2072 (1992).
[24] N. F. Declercq, M. McPherson, M. Breazeale, A. Teklu, “Optical Bragg imaging of acoustic fields after reflection”, J. Acoust. Soc. Am. 127, 3466-3469 (2010).
[25] N. F. Declercq, R. Briers, O. Leroy, “The use of polarized bounded beams to determine the groove direction of a surface corrugation at normal incidence, the generation of surface waves and the insonification at Bragg-angles” Ultrasonics 40, 345-348 (2002).
[26] A. Fasano, M. Primicerio, A. Tesi, “A mathematical model for spaghetti cooking with free boundaries”, Netw. Heterog. Media. 6, 37-60 (2011).
[27] S. Mercier, S. Villeneuve, M. Mondor, L. P. Des Marchais, “Evolution of porosity, shrinkage and density of pasta fortified with pea protein concentrate during drying”, LWT-Food Sci. Technol. 44, 883-890 (2011).
[28] S. Chillo, D. V. Ranawana, C. J. K. Henry, “Effect of two barley beta-glucan concentrates on in vitro glycaemic impact and cooking quality of spaghetti”, LWT-Food Sci. Technol. 44, 940-948 (2011).
[29] A. Baiano, C. Lamacchia, C. Fares, C. Terracone, E. La Notte, “Cooking behaviour and acceptability of composite pasta made of semolina and toasted or partially defatted soy flour”, LWT-Food Sci. Technol. 44, 1226-1232 (2011).
[30] K. Nachay, “Enhancing pasta with peanut flour”, Food Technol-Chicago 65, 14-14 (2011).
[31] W. A. Grandia, C. M. Fortunko, “NDE applications of air-coupled ultrasonic transducers”, 1995 IEEE Ultrasonic Symposium Proceeding, 697-709 (1995).
[32] E. Blomme, D. Bulcaen, F. Declercq, “Recent observation with air-coupled NDE in the frequency range fo 650kHz to 1.2 MHz”, Ultrasonics 40, 153-157 (2002).
[33] E. Blomme, D. Bulcaen, E. Declercq, P. Lust, “Air-coupled ultrasonic testing of textile products”, Emerging Technologies in Non Destructive Testing, 95-100 (2004).
[34] M. Rheinfurth, F. Schmidt, D. Doering, I. Solodov, G. Busse, P. Horst, “Aircoupled guided waves combined with thermography for monitoring fatigue in biaxially loaded composite tubes”, Compos. Sci. Technol. 71, 600-608 (2011).
[35] F. Siegmund, D. Doering, M. Rheinfurth, E. Haberstroh, G. Busse, “Air-coupled ultrasound for monitoring the production of PUR sandwich structures”, Int. Polym. Proc. 25, 372-378 (2010).
[36] H. Tat, G. Georgeson, R. Bossi, “Evalution of air coupled ultrasound for composite aerospace structure”, Review of Progress in Quantitative Nondestructive Evaluation 1096, 912-919 (2009).
[37] K. Berketis, D. Tzetzis, P. J. Hogg, “Impact damage detection and degradation monitoring of wet GFRP composites using noncontact ultrasonics”, Polym. Compos. 30, 1043-1049 (2009).
[38] J. Ealo, J. Camacho, F. Seco, C. Fritsch, “Ultrasonic air-coupled inspection of textible materials using ferroelectret-based phased arrays”, Review of Progress in Quantitative Nondestructive Evaluation 1211, 933-940 (2010).
[39] D. K. Hsu, D. Utrata, M. Monlin Kuo, “NDE of lumber and natural fiber based products with air coupled ultrasound”, Review of Progress in Quantitative Nondestructive Evaluation 1211, 1533-1540 (2010).
[40] T. E. G. Alvarez-Arenas, “Simultaneous determination of the ultrasound velocity and the thickness of solid plates from the analysis of thickness resonances using aircoupled ultrasound”, Ultrasonics 50, 104-109 (2010).
[41] R. Kazys, R. Raisutis, E. Zukauskas, L. Mazeika, A. Vladisauskas, “Air-coupled ultrasonic testing of CFRP rods by means of guided waves”, International Congress on Ultrasonics, Proceedings, Physics Procedia 3, 185-192 (2010).
[42] A. Nichols, K. Attenborough, S. Taherzadeh, “Deduction of static surface roughness from complex excess attenuation”, J. Acoust. Soc. Am. 129, EL89-EL93 (2011).
[43] D. T. Blackstock, “Fundamentals of physical acoustics”, John Wiley & Sons, New York, 2000. Chap. 13, pp 447-449.

## Citations in Chapter V: Ultrasonic Geometrical Characterization of Periodically Corrugated Surfaces

[1] J. A. C. Calleja, N. F. Declercq, “The acoustic raindrop effect at Mexican Pyramids: the architects’ homage to the rain god Chac?” Acta Acust. United Acust. 95 (5), 849-856 (2009).
[2] N. F. Declercq, J. Degrieck, R. Briers, O. Leroy, “A theoretical study of special acoustic effects caused by the staircase of the El Castillo pyramid at the Maya ruins of Chichen-Itza in Mexico”, J. Acoust. Soc. Am. 116 (6), 3328-3335 (2004).
[3] N. F. Declercq, C. S. A. Dekeyser, “Acoustic diffraction effects at the Hellenistic amphitheater of Epidaurus: seat rows responsible for the marvelous acoustics”, J. Acoust. Soc. Am. 121 (4), 2011-2022 (2007).
[4] N. F. Declercq, “Reply on Comment on article ‘Nico F. Declercq et al.: An acoustic diffraction study of a specifically designed auditorium having a corrugated ceiling: Alvar Aalto’s lecture room’”, Acta Acust. United Acust. 97(5), 909-910 (2011).
[5] N. F. Declercq, K. Dewijngaert, K. Vanderhaeghe, P. Verleysen, “An acoustic diffraction study of a specifically designed auditorium having a corrugated ceiling : Alvar Aalto’s lecture room”, Acta Acust. United Acust. 97(4), 599-606 (2011).
[6] A. Talneau, N. Bouadma, Y. Lebellego, S. Slempkes, A. Ougazzaden, G. Patriarche, B. Sermage, “Low-Damage dry-etched grating on an MQW active layer and dislocationfree InP regrowth for $1.55 \mu \mathrm{~m}$ complex-coupled DFB laser fabrication”, IEEE Photonics Technol. Lett. 10 (8), 1070-1072 (1998).
[7] G. V. Blessing, J. A. Slotwinski, D. G. Eitzen, H. M. Ryan, “Ultrasonic measurements of surface roughness”, Appl. Optics 32 (19), 3433-3437 (1993).
[8] Y. C. Shin, S. J. Oh, S. A. Coker, “Surface roughness measurement by ultrasonic sensing for in-process monitoring”, J. Eng. Ind. 117, 439-447 (1995).
[9] J. F. Liu, , N. F. Declercq, “Air-Coupled ultrasonic investigation of stacked cylindrical rods”, J. Acoust. Soc. Am. 131 (6), 4500-4507 (2012).
[10] A. Jungman, L. Adler, G. Quentin, “Ultrasonic anomalies in the spectrum of acoustic waves diffracted by periodic interfaces”, J. Appl. Phys. 53 (7), 4673-4680 (1982).
[11] R. W. Wood, “On a remarkable case of uneven distribution of light in a diffraction grating spectrum”, Philos. Mag. 4, 396-402 (1902).
[12] K. Mampaert, O. Leroy, “Reflection and transmission of normally incident ultrasonic waves on periodic solid-liquid interfaces”, J. Acoust. Soc. Am. 83 (4), 1390-1398 (1988).
[13] J. M. Claeys, O. Leroy, “Diffraction of ultrasonic waves from periodically rough liquid-solid surface”, J. Appl. Phys. 54 (10), 5657-5662 (1983).
[14] A. Jungman, L. Adler, J. Achenbach, R. Roberts, “Reflection from a boundary with periodic roughness: Theory and experiment”, J. Acoust. Soc. Am. 74 (3), 1025-1032 (1983).
[15] M. de Billy, J. Doucet, G. Quentin, “Angular dependence of the backscattered intensity of acoustic waves from rough surfaces”, Ultrasonics International 1975 Conference Proceedings, IPC Sci. Tech., Guilford, pp. 218-223 (1975).
[16] J. T. Fokkema, “Reflection and transmission of elastic waves by the spatially periodic interface between two solids (Theory of the integral equation method)”, Wave Motion 2 (4), 375-393 (1980).
[17] J. T. Fokkema, “Reflection and transmission of elastic waves by the spatially periodic interface between two solids (Numerical results for the sinusoidal interface)”, Wave Motion 3 (1), 33-48 (1981).
[18] R. F. Millar, “The Rayleigh hypothesis and a related least-squares solution to scattering problems for periodic surfaces and other scatterers”, Radio Sci. 8(8,9), 785-796 (1973).
[19] B. A. Lippmann, “Note of the theory of grating”, J. Opt. Soc. Am. 43, 408 (1953).
[20] A. Wirgin, “Reflection from a corrugated surface”, J. Acoust. Soc. Am., 68(2), 692-699 (1980).
[21] D. H. Berman, J. S. Perkins, “Rayleigh method for scattering from random and deterministic interfaces”, J. Acoust. Soc. Am., 88 (2), 1032-1044 (1990).
[22] P. Reinholdtsen, C.H. Chou, B.T. Khuriyakub, “The effects of surface-roughness on subsurface defect detection using acoustic microscopy”, IEEE Trans. Ultrason., Ferroelectr. Freq. Control 33 (1), 104 (1986).
[23] A. A. Luchvich, S. A. Novikov, G. I. Khilko, “Surface-Rough evaluation by acoustic microscopy”, Russ. J. Nondestr. Test. 29 (2), 106-112 (1993).
[24] L. Robert, B. Cretin, “Determination of the observation depth in scanning microdeformation microscopy”, Surf. Interface Anal. 27 (5-6), 568-571 (1999).
[25] R. Gr. Naev, Acoustic Microscopy: Fundamentals and Applications, Wiley-VCH Verlag GmbH & Co. KGaA, Weinheim, p. 16, 2008.
[26] H. T. O’Nell, “Theory of focusing radiators”, J. Acoust. Soc. Am. 21 (5), 516-526 (1949).
[27] L. W. Couch II, Digital and Analog Communication Systems, fifth ed., Prentice-Hall, New Jersey, p. 50, 1993.

## Citations in Chapter VI: Spectral Analysis of the Impact Defects in Composite Plates

[1] S. Qin, M. Omar and D. R. Shan, “Ultrasonic NDE techniques for impact damage inspection on CFRP laminates”, Journal of Materials Science Research, 1 (1), 2-10 (2012).
[2] K. Berketis, D. Tzetzis, J. Hogg, “Impact damage detection and degradation monitoring of wet GFRP composites using noncontact ultrasonics”, Polymer Composites, 30 (8), 1043-1049 (2009).
[3] S. C. Wooh and I. M. Danial, “Enhancement techniques for ultrasonic nondestructive evaluation of composite materials”, Journal of Engineering Materials and Technology, 112 (2), 175 (1990).
[4] A. Tarantola, B. Valette, “Inverse problems = quest for information”, Journal of Geophysics, 50, 159-170 (1982).
[5] N. Bochud, A. A. Fahim, Á. M. Gómez and G. Rus, “Impact damage characterization in composites using signal processing techniques”, Prodedia Engineering, 14, 169-176 (2011).
[6] S. K. Sin and C. H. Chen, “A comparison of deconvolution techniques for ultrasonic evaluation of materials”, IEEE Transactions on Image Processing, 1 (1), 3-10 (1992).
[7] S. C. Wooh and C. Wei, “Cepstrum-based deconvolution of ultrasonic pulse-echo signals from laminated composite materials”, Proceedings of the 12th Engineering Mechanics Conference, ASME, La Jolla, 1-4 (1998).
[8] J. Liu and N. F. Declercq, “Comparison of different approaches in characterization of impact defects of composite plates”, Proceedings of the Acoustics 2012 Nantes Conference, 2659-2663 (2012).

## Citations in Chapter VII:

[1] D. P. Chen, N. M. Wu, Z. Zhang, Y. Li, X. X. Li and C. L. Zhang, “Detection of impact damageds in CFRP composites using burst phase thermography”, Materials Science Forum 689, 282-288 (2011).
[2] K. Berketis, D. Tzetzis, and P. J. Hogg, “Impact damage detection and degradation monitoring of wet GFRP composites using noncontact ultrasonics”, Polymer Composites, 30 (8), 1043-1049 (2009).
[3] P. Li, X. J. Gao, L. Yan, H. P. Kong, Z. H. Zhao, Z. Zhang, “Defect monitoring of CFRP with ultrasonic c-scan method”, Advanced Materials Research, 243-249, 5343-5348 (2011).
[4] S. Qin, M. Omar, D. R. Shan, “Ultrasonic NDE techniques for impact damage inspection on CFRP laminates”, Journal of Materials Science Research, 1(1) (2012).

## Citations in Chapter VIII: Summary and Future Work

[1] J. Liu and N. F. Declercq, “Pulsed ultrasonic comb filtering effect and its application in the measurement of sound velocity and thickness of thin plates”, submitted to IEEE Trans. Ultrason., Ferroelectr., Freq. Control..
[2] R. F. Humphryes and E. A. Ash, “Acoustic bulk-surface-wave transducer”, Electron. Lett. 5, 175 (1969).
[3] E. A. Ash, R. M. de la Rue, and R. F. Humphryes, “Microsound surface waveguide”, IEEE Trans. Microwave Theory Tech. 17, 882 (1969).

---

1. [↩︎](about:blank#fnref1)
    - This value is given by the manufacturer, not measured using ultrasonic technique.
2. (*) values are obtained with the technique using TOF only.[↩︎](about:blank#fnref2)