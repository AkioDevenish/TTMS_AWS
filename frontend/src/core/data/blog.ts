interface lists {
    title: string,
    date: string,
    month: string,
    hits: string,
    img: string,
    desc: string
}
interface detail {
    imge: string,
    title: string,
    desc: string,
    date: string,
    hits: string
}
interface singl {
    imge: string,
    name: string,
    dep: string,
    hits: string,
    comments: string,
    desc: string
}
export const list: lists[] = [
    {
        title: "Encounter every day.",
        date: "02",
        month: "January 2024",
        hits: "0",
        img: "blog/blog-2.jpg",
        desc: "A huge part of it is the incomparable beauty you can encounter every day."
    },
    {
        title: "White color is important.",
        date: "03",
        month: "January 2024",
        hits: "02",
        img: "blog/blog-3.jpg",
        desc: "The simplest things are the most profound. People just don't do it anymore."
    }
]
export const details: detail[] = [
    {
        imge: "blog/blog-5.jpg",
        title: "Black color is important.",
        desc: "A huge part of it is the incomparable beauty you can encounter every day.People just anymore profound.",
        date: "20 April 2024",
        hits: "0"
    },
    {
        imge: "blog/blog-6.jpg",
        title: "Women's Jacket",
        desc: "People just don't do it anymore. We have to change that. Sometimes the simplest things are the most profound.",
        date: "19 April 2024",
        hits: "0"
    },
    {
        imge: "blog/blog-5.jpg",
        title: "Black color is important.",
        desc: "A huge part of it is the incomparable beauty you can encounter every day.People just anymore profound.",
        date: "15 April 2024",
        hits: "0"
    },
    {
        imge: "blog/blog-6.jpg",
        title: "Women's Jacket",
        desc: "People just don't do it anymore. We have to change that. Sometimes the simplest things are the most profound.",
        date: "11 April 2024",
        hits: "0"
    }
]
export const single: singl[] = [
    {
        imge: "blog/4.jpg",
        name: "Jhon Quil",
        dep: "Developer",
        hits: "06",
        comments: "158",
        desc: "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text."
    },
    {
        imge: "blog/12.png",
        name: "Mark Ateer",
        dep: "Designer",
        hits: "08",
        comments: "418",
        desc: "From the east coast to the west, each river has its own beauty and character. Each river has its own story. There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text."
    },
    {
        imge: "blog/14.png",
        name: "Greg Arias",
        dep: "Developer",
        hits: "02",
        comments: "428",
        desc: "Harpeth rises in the westernmost part of Rutherford County, just to the east of the community of College Grove in eastern Williamson County.but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text."
    }
]