interface item {
    col: string,
    title: string,
    desc: string,
    icon: string
}
interface simpleaccordion {
    hederid?: string;
    id: string;
    ids?: string;
    title: string;
    one?: boolean;
    two?: boolean;
    three?: boolean;
    isActive: boolean,
    childern?: Child[];
}
interface Child {
    desc?: string;
    title?: string;
}
interface late {
    icon: string,
    title: string,
    time: string
}
interface featured {
    imge: string,
    title: string,
    desc: string,
    date: string,
    star: number,

}
interface articles {
    title: string,
    icon: string,
    desc: string
}
export const wid: item[] = [
    {
        col: "col-xl-4 box-col-6",
        title: "Articles",
        desc: "How little experience or technical knowledge you currently have. The web is a very big place, and if you are the typical internet user, you probably visit several websites every day.",
        icon: "file-text"
    },
    {
        col: "col-xl-4 col-sm-6 box-col-6",
        title: "Knowledgebase",
        desc: "A Website Designing course enables learners to use essential designing and programming in tools required to do the job. The curriculum is a blend of various themes.",
        icon: "book-open"
    },
    {
        col: "col-xl-4 col-sm-6 box-col-12",
        title: "Support",
        desc: "The customer support industry is renaissance. Customer support as a specialty is coming into its own, offering companies a competitive advantage that’s difficult to copy.",
        icon: "aperture"
    }
]
export const quik: simpleaccordion[] = [
    {
        id: "#collapseicon",
        ids: "collapseicon",
        title: "Integrating WordPress with Your Website?",
        isActive: false,
        childern: [
            {
                title: "How you approach this process will depend on which web host you use. For example, a lot of hosting providers use cPanel, which includes an option to set up subdomains with just a few clicks."
            }
        ]
    },
    {
        id: "#collapseicon2",
        ids: "collapseicon2",
        title: "WordPress Site Maintenance ?",
        isActive: false,
        childern: [
            {
                title: "We’ve just published a detailed on how to backup your WordPress website, however, if you’re in a hurry, here’s a quick solution."
            }
        ]
    },
    {
        id: "#collapseicon3",
        ids: "collapseicon3",
        title: "Meta Tags in WordPress ?",
        isActive: false,
        childern: [
            {
                title: "Manually adding meta tags in WordPress is relatively simple. For this demo, we’ll use the example from the WordPress Codex. Imagine you’re Harriet Smith, a veterinarian who blogs about their animal stories on WordPress."
            }
        ]
    },
    {
        id: "#collapseicon4",
        ids: "collapseicon4",
        title: " WordPress in Your Language ?",
        isActive: false,
        childern: [
            {
                title: "As of version 4.0, you can have WordPress automatically install the language of your choice during the installation process."
            }
        ]
    },
]
export const intell: simpleaccordion[] = [
    {
        id: "#collapseicon5",
        ids: "collapseicon5",
        title: "WordPress Site Maintenance ?",
        isActive: false,
        childern: [
            {
                title: "We’ve just published a detailed on how to backup your WordPress website, however, if you’re in a hurry, here’s a quick solution."
            }
        ]
    },
    {
        id: "#collapseicon6",
        ids: "collapseicon6",
        title: " WordPress in Your Language ?",
        isActive: false,
        childern: [
            {
                title: "As of version 4.0, you can have WordPress automatically install the language of your choice during the installation process."
            }
        ]
    },
    {
        id: "#collapseicon7",
        ids: "collapseicon7",
        title: "Integrating WordPress with Your Website ?",
        isActive: false,
        childern: [
            {
                title: "How you approach this process will depend on which web host you use. For example, a lot of hosting providers use cPanel, which includes an option to set up subdomains with just a few clicks."
            }
        ]
    }
]
export const selling: simpleaccordion[] = [
    {
        id: "#collapseicon8",
        ids: "collapseicon8",
        title: "WordPress Site Maintenance ?",
        isActive: false,
        childern: [
            {
                title: "We’ve just published a detailed on how to backup your WordPress website, however, if you’re in a hurry, here’s a quick solution."
            }
        ]
    },
    {
        id: "#collapseicon9",
        ids: "collapseicon9",
        title: "Meta Tags in WordPress ?",
        isActive: false,
        childern: [
            {
                title: "Manually adding meta tags in WordPress is relatively simple. For this demo, we’ll use the example from the WordPress Codex. Imagine you’re Harriet Smith, a veterinarian who blogs about their animal stories on WordPress."
            }
        ]
    },
    {
        id: "#collapseicon10",
        ids: "collapseicon10",
        title: "Validating a Website ?",
        isActive: false,
        childern: [
            {
                title: "Validating a website is the process of ensuring that the pages on the website conform to the norms or standards defined by various organizations."
            }
        ]
    },
    {
        id: "#collapseicon11",
        ids: "collapseicon11",
        title: " Know Your Sources ?",
        isActive: false,
        childern: [
            {
                title: "A book or set of books giving information on many subjects or on many aspects of one subject. Some are intended as an entry point into research for a general audience, some provide detailed information."
            }
        ]
    },
]
export const users: simpleaccordion[] = [
    {
        id: "#collapseicon12",
        ids: "collapseicon12",
        title: "Integrating WordPress with Your Website ?",
        isActive: false,
        childern: [
            {
                title: "How you approach this process will depend on which web host you use. For example, a lot of hosting providers use cPanel, which includes an option to set up subdomains with just a few clicks."
            }
        ]
    },
    {
        id: "#collapseicon13",
        ids: "collapseicon13",
        title: "WordPress Site Maintenance ?",
        isActive: false,
        childern: [
            {
                title: "We’ve just published a detailed on how to backup your WordPress website, however, if you’re in a hurry, here’s a quick solution."
            }
        ]
    },
    {
        id: "#collapseicon14",
        ids: "collapseicon14",
        title: "WordPress in Your Language ?",
        isActive: false,
        childern: [
            {
                title: "As of version 4.0, you can have WordPress automatically install the language of your choice during the installation process."
            }
        ]
    },
    {
        id: "#collapseicon15",
        ids: "collapseicon15",
        title: "Validating a Website ?",
        isActive: false,
        childern: [
            {
                title: "Validating a website is the process of ensuring that the pages on the website conform to the norms or standards defined by various organizations."
            }
        ]
    },
    {
        id: "#collapseicon16",
        ids: "collapseicon16",
        title: "Meta Tags in WordPress ?",
        isActive: false,
        childern: [
            {
                title: "Manually adding meta tags in WordPress is relatively simple. For this demo, we’ll use the example from the WordPress Codex. Imagine you’re Harriet Smith, a veterinarian who blogs about their animal stories on WordPress."
            }
        ]
    },
]
export const latest: late[] = [
    {
        icon: "rotate-cw",
        title: "<a href='#'>David Linner </a>requested money back for a double debit card charge",
        time: "10 minutes ago"
    },
    {
        icon: "dollar-sign",
        title: "All sellers have received monthly payouts",
        time: "2 hours ago"
    },
    {
        icon: "link",
        title: "User Christopher <a href='#'>Wallace</a> is on hold and awaiting for staff reply",
        time: "45 minutes ago"
    },
    {
        icon: "check",
        title: "Ticket #43683 has been closed by <a href='#'>Victoria Wilson</a>",
        time: "Dec 7, 11:48"
    }
]
export const featured: featured[] = [
    {
        imge: "faq/1.jpg",
        title: "Web Design",
        desc: "A Web Designing course belongs to the field of Computer Science and IT. It enables students to learn.",
        date: "Dec 15, 2024",
        star: 5,

    },
    {
        imge: "faq/2.jpg",
        title: "Web Development",
        desc: "This course is designed to start you on a path toward future studies in web development and design.",
        date: "Mar 02, 2024",
        star: 4,

    },
    {
        imge: "faq/3.jpg",
        title: "UI Design",
        desc: "User interface design (UI) is the design for machines and software, such as mobile devices, computers.",
        date: "Feb 04, 2024",
        star: 5,

    },
    {
        imge: "faq/4.jpg",
        title: "UX Design",
        desc: "A Web Designing course belongs to the field of Computer Science and IT. It enables students to learn.",
        date: "Jan 18, 2024",
        star: 4,

    }
]
export const articles: articles[] = [
    {
        title: "Article Base Video",
        icon: "codepen",
        desc: "The web is a very big place, and if you are the typical internet user."
    },
    {
        title: "Knows your sources",
        icon: "codepen",
        desc: "A book giving information on many subjects or on many aspects of one subject."
    },
    {
        title: "Sources credible/reliable",
        icon: "codepen",
        desc: "Simple demos of frequently asked questions about using the information resources"
    }
]
export const articles1: articles[] = [
    {
        title: "Validate website",
        icon: "file-text",
        desc: "Website is the process of ensuring that the pages on the website conform."
    },
    {
        title: "Tailwind Design",
        icon: "file-text",
        desc: "Tailwind is so low-level, it never encourages you to design the same site twice."
    },
    {
        title: "Knows your sources",
        icon: "file-text",
        desc: "A book giving information on many subjects or on many aspects of one subject."
    }
]
export const articles2: articles[] = [
    {
        title: "Sources Demos",
        icon: "youtube",
        desc: "Simple demos of frequently asked questions about using the information resources"
    },
    {
        title: "Validate Html",
        icon: "youtube",
        desc: "Website is the process of ensuring that the pages on the website conform."
    },
    {
        title: "Web Design",
        icon: "youtube",
        desc: "Web is so high-level, it never encourages you to design the same site twice"
    }
]