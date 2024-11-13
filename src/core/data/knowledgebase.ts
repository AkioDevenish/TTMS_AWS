interface item {
    col: string,
    title: string,
    desc: string,
    icon: string
}
interface categorys {
    articles: string,
    articles1: string,
    articles2: string,
    articles3: string,
    articles4: string,
    see: string
}
interface featureds {
    imge: string,
    title: string,
    desc: string,
    date: string,
    star: number
}
export const wid: item[] = [
    {
        col: "col-xl-4 box-col-6",
        title: "Support",
        desc: "The customer support industry is renaissance. Customer support as a specialty is coming into its own, offering companies a competitive advantage that’s difficult to copy.",
        icon: "aperture"
    },
    {
        col: "col-xl-4 col-sm-6",
        title: "Knowledgebase",
        desc: "A Website Designing course enables learners to use essential designing and programming in tools required to do the job. The curriculum is a blend of various themes.",
        icon: "book-open"
    },
    {
        col: "col-xl-4",
        title: "Articles",
        desc: "How little experience or technical knowledge you currently have. The web is a very big place, and if you are the typical internet user, you probably visit several websites every day.",
        icon: "file-text"
    }
]
export const category: categorys[] = [
    {
        articles: "Any other legal pages I should know about?",
        articles1: "Policies have wide acceptance among editors",
        articles2: "Guidelines are sets of best practices supported.",
        articles3: "Editors should attempt to follow guidelines. ",
        articles4: "They are best treated with common sense.",
        see: "40"
    },
    {
        articles: "Does Moment have an API or automatic export?",
        articles1: "Resource API content produced by business. ",
        articles2: "API allows the search and download of AP Images.",
        articles3: "API retrieve a list of breaking news categories",
        articles4: "API retrieves rules for a fantasy league.",
        see: "90"
    },
    {
        articles: "WordPress Site Maintenance",
        articles1: "Make a backup of your WordPress website.",
        articles2: "Run a security check.  ",
        articles3: "Monitor your search engine optimization.",
        articles4: "Set a regular maintenance schedule.",
        see: "40"
    },
    {
        articles: "Can I change my plan later?",
        articles1: "You can easily change plans Wonderfull at any time.",
        articles2: "you’ll be charged a prorated cover that upgrade.",
        articles3: "But also the leap into electronic typesetting, ",
        articles4: "When an unknown printer took a galley",
        see: "90"
    },
    {
        articles: "How do I pay for the Premium Plan?",
        articles1: "Premium plans are billed as a yearly payment",
        articles2: "Monthly plan are bill every month date of your signup.",
        articles3: "You can set Monthly or Yearly for Premium plan.",
        articles4: "When an unknown printer took a galley",
        see: "50"
    },
    {
        articles: "What is your Shopping Policy",
        articles1: "Many new editors rely on policy interpretations.",
        articles2: "Editor continually attempts to find a different policy.",
        articles3: "Violation of maintaining a neutral point of view.",
        articles4: "You double check your sources.",
        see: "26"
    },
    {
        articles: "How can I change the component?",
        articles1: "You can modify some specific component settings. ",
        articles2: "Click Apply to validate the set preferences.",
        articles3: "Following procedure applie to external components ",
        articles4: "To modify those specific components settings.",
        see: "10"
    },
    {
        articles: "How does it work?",
        articles1: "To get started with your account. ",
        articles2: "Editor continually attempts to find a different policy",
        articles3: "Users can browse by topic or use the visually. ",
        articles4: "This works through various methods of site tracking",
        see: "21"
    },
    {
        articles: "What is Lorem Ipsum?",
        articles1: "Common language regular than the existing languages.",
        articles2: "Lorem Ipsum has been the industry's standard dummy",
        articles3: "Language is not real even ‘Lorem’ does't exist.",
        articles4: "dummy text that is not meant to mean anything",
        see: "34"
    }
]
export const featured: featureds[] = [
    {
        imge: "faq/1.jpg",
        title: "Web Design",
        desc: "A Web Designing course belongs to the field of Computer It enables students to learn various techniques.",
        date: "Dec 15, 2024",
        star: 2
    },
    {
        imge: "faq/2.jpg",
        title: "Web Development",
        desc: "A Web Development course belongs to the field of Computer It enables students to learn various techniques.",
        date: "Jan 08, 2024",
        star: 3
    },
    {
        imge: "faq/3.jpg",
        title: "UI Design",
        desc: "User interface design (UI) is the design for machines and software, such as mobile devices, computers.",
        date: "Feb 15, 2024",
        star: 1
    },

    {
        imge: "faq/3.jpg",
        title: "UX Design",
        desc: "User Experience design (UX) is the design for machines and software, such as mobile devices, computers.",
        date: "Sept 10, 2024",
        star: 2
    }
]