keyword_list = {
    'IF': {
        'Exception':[[('Word',-1,'EVEN')],[('Word',-1,'AS')],[('Word',1,'ONLY')],[('Verb','Next','Past')]]
    },
    'UNLESS': {
    },
    'UNTIL':{
    },
    'PROVIDED':{
        'Composite':[[('Word',-1,'THAT')]]
    },
    'ASSUMING':{
        'Composite':[[('Word',1,'THAT')]]
    },
    'OTHERWISE':{
    },
    'WHEN':{
        'Exception':[[('Verb','Next','Past')],[('Word','Any','WILL')]]
    },
    'BECAUSE':{
        'Exception':[[('Verb','Next','Past')]]
    },
    'SO':{
        'Exception':[[('Word',1,'FAR')]]
    },
    'BY':{
        'Composite':[[('Verb',1,'-ing')]]
    },
    'AS':{
        'Composite':[[('Upos',1,'PRON')],[('Upos',1,'PROPN')],[('Upos',1,'NOUN')]], 'Exception':[[('Word',2,'AS')],[('Word',-2,'AS')],[('Word',1,'IF')],[('Verb','Next','Past')]]
    },
    'CREATE':{
    },
    'CREATES':{
    },
    'DUE':{
        'Composite':[[('Word',1,'TO')]]
    },
    'LEAD':{
        'Composite':[[('Word',1,'TO')]]
    },
    'INSTEAD':{
    }
}
