
int main() {
    float out[2][4][4];
    float x[2][3][4][4] = {
        {
            {
                {0.49671415, -0.1382643, 0.64768854, 1.52302986},
                {-0.23415337, -0.23413696, 1.57921282, 0.76743473},
                {-0.46947439, 0.54256004, -0.46341769, -0.46572975},
                {0.24196227, -1.91328024, -1.72491783, -0.56228753}
            },
            {
                {-1.01283112, 0.31424733, -0.90802408, -1.4123037},
                {1.46564877, -0.2257763, 0.0675282, -1.42474819},
                {-0.54438272, 0.11092259, -1.15099358, 0.37569802},
                {-0.60063869, -0.29169375, -0.60170661, 1.85227818}
            },
            {
                {-0.01349722, -1.05771093, 0.82254491, -1.22084365},
                {0.2088636, -1.95967012, -1.32818605, 0.19686124},
                {0.73846658, 0.17136828, -0.11564828, -0.3011037},
                {-1.47852199, -0.71984421, -0.46063877, 1.05712223}
            }
        },
        {
            {
                {0.34361829, -1.76304016, 0.32408397, -0.38508228},
                {-0.676922, 0.61167629, 1.03099952, 0.93128012},
                {-0.83921752, -0.30921238, 0.33126343, 0.97554513},
                {-0.47917424, -0.18565898, -1.10633497, -1.19620662}
            },
            {
                {0.81252582, 1.35624003, -0.07201012, 1.0035329},
                {0.36163603, -0.64511975, 0.36139561, 1.53803657},
                {-0.03582604, 1.56464366, -2.6197451, 0.8219025},
                {0.08704707, -0.29900735, 0.09176078, -1.98756891}
            },
            {
                {-0.21967189, 0.35711257, 1.47789404, -0.51827022},
                {-0.8084936, -0.50175704, 0.91540212, 0.32875111},
                {-0.5297602, 0.51326743, 0.09707755, 0.96864499},
                {-0.70205309, -0.32766215, -0.39210815, -1.46351495}
            }
        }
    };

    float W[3][3][3][2] = {
    {
        {
            {0.29612028, 0.26105527},
            {0.00511346, -0.23458713},
            {-1.41537074, -0.42064532}
        },
        {
            {-0.34271452, -0.80227727},
            {-0.16128571, 0.40405086},
            {1.8861859, 0.17457781}
        },
        {
            {0.25755039, -0.07444592},
            {-1.91877122, -0.02651388},
            {0.06023021, 2.46324211}
        }
    },
    {
        {
            {-0.19236096, 0.30154734},
            {-0.03471177, -1.16867804},
            {1.14282281, 0.75193303}
        },
        {
            {0.79103195, -0.90938745},
            {1.40279431, -1.40185106},
            {0.58685709, 2.19045563}
        },
        {
            {-0.99053633, -0.56629773},
            {0.09965137, -0.50347565},
            {-1.55066343, 0.06856297}
        }
    },
    {
        {
            {-1.06230371, 0.47359243},
            {-0.91942423, 1.54993441},
            {-0.78325329, -0.32206152}
        },
        {
            {0.81351722, -1.23086432},
            {0.22745993, 1.30714275},
            {-1.60748323, 0.18463386}
        },
        {
            {0.25988279, 0.78182287},
            {-1.23695071, -1.32045661},
            {0.52194157, 0.29698467}
        }
    }
};

    float b[2] = {0.25049285, 0.34644821};

    int stride = 1;
    int pad = 1;

    conv_layer(x, out, W, b, stride, pad);

    // Print the output
    for (int n = 0; n < 2; n++) {
        for (int f = 0; f < 2; f++) {
            for (int i = 0; i < 4; i++) {
                for (int j = 0; j < 4; j++) {
                    printf("%.8f ", out[n*2*4*4 + f*4*4 + i*4 + j]);
                }
                printf("\n");
            }
            printf("\n");
        }
    }

    free(out);
    return 0;
}