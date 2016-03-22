from toolshare.models.reservation import Reservation


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def is_valid_name(name):
    for c in name:
        if c.isalpha():
            pass
        else:
            if c == ' ':
                pass
            else:
                return False
    return True

class EmailSender(object):

    @staticmethod
    def send_email(email, subject, msg=None):
        pass

    @staticmethod
    def send_cancel_request_email(reservation):
        # Prepare the Borrow-message
        msg_buff = list()
        msg_buff.append('Dear {requester}')
        msg_buff.append('')
        msg_buff.append('Your request for the tool: {tool} between {start_date} - {end_date}, was cancelled by the owner: {owner}')
        msg_buff.append('She/He has ')
        msg_buff.append('left the following message:')
        msg_buff.append('')
        msg_buff.append('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        msg_buff.append('{cancel_msg}')
        msg_buff.append('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        msg_buff.append('')
        msg_buff.append('----')
        msg_buff.append('ToolShare Team')
        msg = '\n'.join(msg_buff)
        msg = msg.format(owner=reservation.lender.get_full_name(),
                         requester=reservation.borrower.get_full_name(),
                         tool=reservation.tool.name,
                         start_date=reservation.start_date,
                         end_date=reservation.end_date,
                         cancel_msg=reservation.cancel_msg)

        # Send the email
        EmailSender.send_email(email=reservation.lender.email,
                               subject="Borrow your tool",
                               msg=msg)

        # Output the email on the screen
        print("Cancel-Request-Email:")
        print("\n%s" % msg)

    @staticmethod
    def send_borrow_request_email(reservation):
        # Prepare the Borrow-message
        msg_buff = list()
        msg_buff.append('Dear {owner}')
        msg_buff.append('')
        msg_buff.append('{requester} wants to borrow your tool: {tool},')
        msg_buff.append('between {start_date} - {end_date}. She/He has ')
        msg_buff.append('left the following message:')
        msg_buff.append('')
        msg_buff.append('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        msg_buff.append('{request_msg}')
        msg_buff.append('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        msg_buff.append('')
        if not reservation.is_approved():
            msg_buff.append('You can approve/reject this by clicking '
                            '<a href="http://127.0.0.1:8000/toolshare/borrow-tool/{tool_id}">here</a>')
            msg_buff.append('')
        msg_buff.append('----')
        msg_buff.append('ToolShare Team')
        msg = '\n'.join(msg_buff)
        msg = msg.format(owner=reservation.lender.get_full_name(),
                         requester=reservation.borrower.get_full_name(),
                         tool=reservation.tool.name,
                         start_date=reservation.start_date,
                         end_date=reservation.end_date,
                         request_msg=reservation.request_msg,
                         tool_id = reservation.tool.id)

        # Send the email
        EmailSender.send_email(email=reservation.lender.email,
                               subject="Borrow your tool",
                               msg=msg)

        # Output the email on the screen
        print("Borrow-Request-Email:")
        print("\n%s" % msg)

    @staticmethod
    def send_approve_reject_request_email(reservation):
        # Prepare the Borrow-message
        status = reservation.get_status_description()
        if reservation.status == 'A':
            the_msg = 'Hey. I approved your request'
        elif reservation.status == 'R':
            the_msg = reservation.reject_msg
        else:
            the_msg = ''
        msg_buff = list()
        msg_buff.append('Dear {requester}')
        msg_buff.append('')
        msg_buff.append('Your request for the tool: {tool} between {start_date} - {end_date}, was {status} by the owner: {owner}')
        msg_buff.append('She/He has ')
        msg_buff.append('left the following message:')
        msg_buff.append('')
        msg_buff.append('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        msg_buff.append('{msg}')
        msg_buff.append('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        msg_buff.append('')
        msg_buff.append('----')
        msg_buff.append('ToolShare Team')
        msg = '\n'.join(msg_buff)
        msg = msg.format(owner=reservation.lender.get_full_name(),
                         requester=reservation.borrower.get_full_name(),
                         tool=reservation.tool.name,
                         start_date=reservation.start_date,
                         end_date=reservation.end_date,
                         msg=the_msg,
                         status=status)

        # Send the email
        EmailSender.send_email(email=reservation.lender.email,
                               subject=status+" your request-reservation",
                               msg=msg)

        # Output the email on the screen
        print("Approve-Reject-Request-Email:")
        print("\n%s" % msg)

