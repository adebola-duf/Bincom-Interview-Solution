from .models import polling_unit, announced_pu_results, lga
from .db import engine
from sqlmodel import Session, select


def get_all_polling_units_from_polling_units_table() -> list[polling_unit]:
    with Session(engine) as session:
        statement = select(polling_unit)

        results = session.exec(statement)
        list_results = results.all()
        return list_results


get_all_polling_units_from_polling_units_table()


def get_particular_polling_units_from_announced_pu_results_table(polling_unit_uniqueid: str):
    with Session(engine) as session:
        statement = select(announced_pu_results).where(
            announced_pu_results.polling_unit_uniqueid == polling_unit_uniqueid)
        results = session.exec(statement)

        list_results = results.all()
        return list_results


def get_lga_results_from_not_announced_lga_results():
    # lemme first get all the lga ids first they are actually lga name. one thing i could do would be to iterate over everything in polling unit table and then when i am done with that lga, i add it to a list done lga
    # {
    # lga id 19: {
    # "PDP": 900
    # }
    # }
    with Session(engine) as session:
        # polling_unit table is the table taht contains the top level things we need so the pollingunit unique id and the lga id
        statement1 = select(polling_unit)
        all_the_polling_units: list[polling_unit] = session.exec(
            statement1).all()

        polling_unit_id_to_party_results_mapping: dict[int, dict[str, int]] = {
        }
        pu_that_are_under_an_lga: dict[int, list] = {}
        for each_unique_polling_unit in all_the_polling_units:
            # party_results_for_each_polling_unit = {}
            party_results_for_each_polling_unit = session.exec(select(announced_pu_results).where(
                announced_pu_results.polling_unit_uniqueid == str(each_unique_polling_unit.uniqueid))).all()
            # this dict is going to store the party results for each of the unique polling units

            for each_party_result_for_each_polling_unit in party_results_for_each_polling_unit:

                if each_party_result_for_each_polling_unit.polling_unit_uniqueid not in polling_unit_id_to_party_results_mapping:
                    polling_unit_id_to_party_results_mapping[each_party_result_for_each_polling_unit.polling_unit_uniqueid] = {
                        each_party_result_for_each_polling_unit.party_abbreviation: each_party_result_for_each_polling_unit.party_score}
                else:
                    polling_unit_id_to_party_results_mapping[each_party_result_for_each_polling_unit.polling_unit_uniqueid][
                        each_party_result_for_each_polling_unit.party_abbreviation] = each_party_result_for_each_polling_unit.party_score

            if each_unique_polling_unit.lga_id not in pu_that_are_under_an_lga:
                pu_that_are_under_an_lga[each_unique_polling_unit.lga_id] = [
                    each_unique_polling_unit.uniqueid]
            else:
                pu_that_are_under_an_lga[each_unique_polling_unit.lga_id].append(
                    each_unique_polling_unit.uniqueid)

        lga_name_to_lga_id_mapping = {}

        all_lgas = session.exec(select(lga)).all()
        for each_lga in all_lgas:
            lga_name_to_lga_id_mapping[each_lga.lga_name] = each_lga.lga_id

        return polling_unit_id_to_party_results_mapping, pu_that_are_under_an_lga, lga_name_to_lga_id_mapping


def compile_all_polling_unit_results_for_a_local_govenrnment(polling_unit_id_to_party_results_mapping: dict[int, dict[str, int]], pu_that_are_under_an_lga: dict[int, list]):

    lga_party_results = {}  # {19: {"PDP":100000, "APC": 90000}}
    # pu that are under an lga {19: [9, 10, 14, 46], 34: [11, 17, 28, 31, 106, 107]} lga_id: the pu id under that lga
    for lga_id in pu_that_are_under_an_lga.keys():
        for each_pu_unique_id in pu_that_are_under_an_lga[lga_id]:
            # get the party results for that polling unit
            if lga_id not in lga_party_results:
                if (str(each_pu_unique_id)) in polling_unit_id_to_party_results_mapping:
                    lga_party_results[lga_id] = polling_unit_id_to_party_results_mapping[str(
                        each_pu_unique_id)]
            else:
                # each party result reps the party name
                if str(each_pu_unique_id) in polling_unit_id_to_party_results_mapping:
                    for each_party_result in polling_unit_id_to_party_results_mapping[str(each_pu_unique_id)].keys():
                        if each_party_result in lga_party_results[lga_id]:
                            lga_party_results[lga_id][each_party_result] += polling_unit_id_to_party_results_mapping[str(
                                each_pu_unique_id)][each_party_result]
                        else:
                            lga_party_results[lga_id].update(
                                {each_party_result: polling_unit_id_to_party_results_mapping[str(each_pu_unique_id)][each_party_result]})

    return lga_party_results
