interface drop {
    classes: string,
    title: string
}
interface item {
    classes: string,
    checked?: boolean
}
interface RadioButtonGroup {
    group: string;
    options: RadioButton[];
}
interface RadioButton {
    id: string;
    value: string;
    label: string;
    checked?: boolean;
    classes: string
}

export const button: drop[] = [
    {
        classes: "btn-primary",
        title: "Primary Button"
    },
    {
        classes: "btn-secondary",
        title: "Secondary Button"
    },
    {
        classes: "btn-success",
        title: "Success Button"
    },
    {
        classes: "btn-info",
        title: "Info Button"
    },
    {
        classes: "btn-warning",
        title: "Warning Button"
    },
    {
        classes: "btn-danger",
        title: "Danger Button"
    },
    {
        classes: "btn-light",
        title: "Light Button"
    }
]
export const color: drop[] = [
    {
        classes: "btn-outline-primary",
        title: "Primary Button"
    },
    {
        classes: "btn-outline-secondary",
        title: "Secondary Button"
    },
    {
        classes: "btn-outline-success",
        title: "Success Button"
    },
    {
        classes: "btn-outline-info",
        title: "Info Button"
    },
    {
        classes: "btn-outline-warning",
        title: "Warning Button"
    },
    {
        classes: "btn-outline-danger",
        title: "Danger Button"
    },
    {
        classes: "btn-outline-light txt-dark",
        title: "Light Button"
    }
]
export const outline: drop[] = [
    {
        classes: "btn-outline-primary-2x",
        title: "Primary Button"
    },
    {
        classes: "btn-outline-secondary-2x",
        title: "Secondary Button"
    },
    {
        classes: "btn-outline-success-2x",
        title: "Success Button"
    },
    {
        classes: "btn-outline-info-2x",
        title: "Info Button"
    },
    {
        classes: "btn-outline-warning-2x",
        title: "Warning Button"
    },
    {
        classes: "btn-outline-danger-2x",
        title: "Danger Button"
    },
    {
        classes: "btn-outline-light-2x txt-dark",
        title: "Light Button"
    }
]
export const gradien: drop[] = [
    {
        classes: "btn-primary-gradien",
        title: "Primary Button"
    },
    {
        classes: "btn-secondary-gradien",
        title: "Secondary Button"
    },
    {
        classes: "btn-success-gradien",
        title: "Success Button"
    },
    {
        classes: "btn-info-gradien",
        title: "Info Button"
    },
    {
        classes: "btn-warning-gradien",
        title: "Warning Button"
    },
    {
        classes: "btn-danger-gradien",
        title: "Danger Button"
    }
]
export const raised: drop[] = [
    {
        classes: "btn-primary btn-air-primary",
        title: "Primary Button"
    },
    {
        classes: "btn-secondary btn-air-secondary",
        title: "Secondary Button"
    },
    {
        classes: "btn-success btn-air-success",
        title: "Success Button"
    },
    {
        classes: "btn-info btn-air-info",
        title: "Info Button"
    },
    {
        classes: "btn-warning btn-air-warning",
        title: "Warning Button"
    },
    {
        classes: "btn-danger btn-air-danger",
        title: "Danger Button"
    },
    {
        classes: "btn-light btn-air-light",
        title: "Light Button"
    }
]
export const color1: drop[] = [
    {
        classes: "btn-outline-primary btn-air-primary",
        title: "Primary Button"
    },
    {
        classes: "btn-outline-secondary btn-air-secondary",
        title: "Secondary Button"
    },
    {
        classes: "btn-outline-success btn-air-success",
        title: "Success Button"
    },
    {
        classes: "btn-outline-info btn-air-info",
        title: "Info Button"
    },
    {
        classes: "btn-outline-warning btn-air-warning",
        title: "Warning Button"
    },
    {
        classes: "btn-outline-danger btn-air-danger",
        title: "Danger Button"
    },
    {
        classes: "btn-outline-light btn-air-light txt-dark",
        title: "Light Button"
    }
]
export const outline1: drop[] = [
    {
        classes: "btn-outline-primary-2x btn-air-primary",
        title: "Primary Button"
    },
    {
        classes: "btn-outline-secondary-2x btn-air-secondary",
        title: "Secondary Button"
    },
    {
        classes: "btn-outline-success-2x btn-air-success",
        title: "Success Button"
    },
    {
        classes: "btn-outline-info-2x btn-air-info",
        title: "Info Button"
    },
    {
        classes: "btn-outline-warning-2x btn-air-warning",
        title: "Warning Button"
    },
    {
        classes: "btn-outline-danger-2x btn-air-danger",
        title: "Danger Button"
    },
    {
        classes: "btn-outline-light-2x btn-air-light txt-dark",
        title: "Light Button"
    }
]
export const gradien1: drop[] = [
    {
        classes: "btn-primary-gradien btn-air-primary",
        title: "Primary Button"
    },
    {
        classes: "btn-secondary-gradien btn-air-secondary",
        title: "Secondary Button"
    },
    {
        classes: "btn-success-gradien btn-air-success",
        title: "Success Button"
    },
    {
        classes: "btn-info-gradien btn-air-info",
        title: "Info Button"
    },
    {
        classes: "btn-warning-gradien btn-air-warning",
        title: "Warning Button"
    },
    {
        classes: "btn-danger-gradien btn-air-danger",
        title: "Danger Button"
    }
]
export const basic: item[] = [
    {
        classes: "btn-primary"
    },
    {
        classes: "btn-secondary"
    },
    {
        classes: "btn-success"
    },
    {
        classes: "btn-info"
    },
    {
        classes: "btn-warning"
    },
    {
        classes: "btn-danger"
    },
    {
        classes: "btn-light"
    },
    {
        classes: "btn-dark"
    }
]
export const flat: item[] = [
    {
        classes: "btn-primary"
    },
    {
        classes: "btn-secondary"
    },
    {
        classes: "btn-success"
    },
    {
        classes: "btn-info"
    },
    {
        classes: "btn-dark"
    },
    {
        classes: "btn-warning"
    },
    {
        classes: "btn-danger"
    },
    {
        classes: "btn-light"
    },
    {
        classes: "btn-dark"
    }
]
export const common: item[] = [
    {
        classes: "primary"
    },
    {
        classes: "secondary"
    },
    {
        classes: "success"
    },
    {
        classes: "info"
    },
    {
        classes: "warning"
    },
    {
        classes: "danger"
    },
    {
        classes: "light"
    },
    {
        classes: "dark"
    }
]
export const radioButtonData: RadioButtonGroup[] = [
    {
        group: "radio1",
        options: [
            {
                id: "radio7",
                value: "option1",
                label: "Option 1",
                classes: "primary",
            },
            {
                id: "radio8",
                value: "option2",
                label: "Option 2",
                checked: true,
                classes: "primary",
            }
        ]
    },
    {
        group: "radio2",
        options: [
            {
                id: "radio11",
                value: "option1",
                label: "Option 1",
                classes: "secondary",
            },
            {
                id: "radio12",
                value: "option2",
                label: "Option 2",
                checked: true,
                classes: "secondary",
            }
        ]
    },
    {
        group: "radio3",
        options: [
            {
                id: "radio13",
                value: "option1",
                label: "Option 1",
                classes: "success ",
            },
            {
                id: "radio14",
                value: "option2",
                label: "Option 2",
                checked: true,
                classes: "success",
            }
        ]
    },
    {
        group: "radio4",
        options: [
            {
                id: "radio15",
                value: "option1",
                label: "Option 1",
                classes: "info",
            },
            {
                id: "radio16",
                value: "option2",
                label: "Option 2",
                checked: true,
                classes: "info",
            }
        ]
    },
    {
        group: "radio5",
        options: [
            {
                id: "radio17",
                value: "option1",
                label: "Option 1",
                classes: "warning",
            },
            {
                id: "radio18",
                value: "option2",
                label: "Option 2",
                checked: true,
                classes: "warning",
            }
        ]
    },
    {
        group: "radio6",
        options: [
            {
                id: "radio19",
                value: "option1",
                label: "Option 1",
                classes: "danger",
            },
            {
                id: "radio20",
                value: "option2",
                label: "Option 2",
                checked: true,
                classes: "danger",
            }
        ]
    },
    {
        group: "radio7",
        options: [
            {
                id: "radio21",
                value: "option1",
                label: "Option 1",
                classes: "light txt-dark",
            },
            {
                id: "radio22",
                value: "option2",
                label: "Option 2",
                checked: true,
                classes: "light txt-dark",
            }
        ]
    }
]
export const checkButtonData: RadioButtonGroup[] = [
    {
        group: "check1",
        options: [
            {
                id: "checkbox-primary-1",
                value: "option1",
                label: "Option 1",
                classes: "primary",
            },
            {
                id: "checkbox-primary-2",
                value: "option2",
                label: "Option 2",
                checked: true,
                classes: "primary",
            }
        ]
    },
    {
        group: "check2",
        options: [
            {
                id: "checkbox-primary-3",
                value: "option1",
                label: "Option 1",
                classes: "secondary",
            },
            {
                id: "checkbox-primary-4",
                value: "option2",
                label: "Option 2",
                checked: true,
                classes: "secondary",
            }
        ]
    },
    {
        group: "check3",
        options: [
            {
                id: "checkbox-primary-5",
                value: "option1",
                label: "Option 1",
                classes: "success ",
            },
            {
                id: "checkbox-primary-6",
                value: "option2",
                label: "Option 2",
                checked: true,
                classes: "success",
            }
        ]
    },
    {
        group: "check4",
        options: [
            {
                id: "checkbox-primary-7",
                value: "option1",
                label: "Option 1",
                classes: "info",
            },
            {
                id: "checkbox-primary-8",
                value: "option2",
                label: "Option 2",
                checked: true,
                classes: "info",
            }
        ]
    },
    {
        group: "check5",
        options: [
            {
                id: "checkbox-primary-9",
                value: "option1",
                label: "Option 1",
                classes: "warning",
            },
            {
                id: "checkbox-primary-10",
                value: "option2",
                label: "Option 2",
                checked: true,
                classes: "warning",
            }
        ]
    },
    {
        group: "check6",
        options: [
            {
                id: "checkbox-primary-11",
                value: "option1",
                label: "Option 1",
                classes: "danger",
            },
            {
                id: "checkbox-primary-12",
                value: "option2",
                label: "Option 2",
                checked: true,
                classes: "danger",
            }
        ]
    },
    {
        group: "check7",
        options: [
            {
                id: "checkbox-primary-13",
                value: "option1",
                label: "Option 1",
                classes: "light txt-dark",
            },
            {
                id: "checkbox-primary-14",
                value: "option2",
                label: "Option 2",
                checked: true,
                classes: "light txt-dark",
            }
        ]
    }
]