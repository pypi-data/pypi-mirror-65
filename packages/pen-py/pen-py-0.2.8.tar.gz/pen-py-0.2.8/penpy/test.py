from dicplus import DicPlus

mydp = DicPlus({
    "test":"{placeholder}",
    "test2":"{pl2.1}"
})
data_variables= {
    "placeholder":"coucou",
    "pl2":{}
}
mydp.format(data_variables).pprint()
