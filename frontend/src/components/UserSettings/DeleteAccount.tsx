import {
  Button,
  Container,
  Heading,
  Text,
  useDisclosure,
} from "@chakra-ui/react"

import DeleteConfirmation from "./DeleteConfirmation"

const DeleteAccount = () => {
  const confirmationModal = useDisclosure()

  return (
    <>
      <Container maxW="full">
        <Heading size="sm" py={4}>
          Удаление аккаунта
        </Heading>
        <Text>
          Навсегда удалит ваши данные и все что связано с вашим аккаунтом.
        </Text>
        <Button variant="danger" mt={4} onClick={confirmationModal.onOpen}>
          Удалить
        </Button>
        <DeleteConfirmation
          isOpen={confirmationModal.isOpen}
          onClose={confirmationModal.onClose}
        />
      </Container>
    </>
  )
}
export default DeleteAccount
